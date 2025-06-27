import streamlit as st
import pandas as pd
import plotly.express as px

def trend_analysis(data):
    if data is not None:
        # Dashboard Title and subtitle
        st.markdown("<h1 style='text-align: center; color: #4CAF50;'>FLAVOUR FORECAST - Trend Analysis Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Explore trends and visualize the impact of various factors on sales</h4>", unsafe_allow_html=True)
        st.write("---")

        # Sidebar options for customizations
        st.sidebar.markdown("<h2 style='color: #FF7F50;'>Explore Data</h2>", unsafe_allow_html=True)
        st.sidebar.markdown("<p style='font-size: 14px; color: gray;'>Choose chart type, attributes, and date range to analyze trends.</p>", unsafe_allow_html=True)

        # Visualization type selection
        visualization_type = st.sidebar.selectbox("Visualization Type", ["Bar Chart", "Line Chart", "Pie Chart", "Heatmap", "Boxplot", "Scatterplot"])

        # X-axis and Y-axis attribute selection
        x_axis = st.sidebar.selectbox("X-axis", data.columns, help="Select the attribute for the X-axis.")
        y_axis = st.sidebar.selectbox("Y-axis", data.columns, help="Select the attribute for the Y-axis.")

        # Date range filter
        st.sidebar.markdown("<h3 style='color: #FF7F50;'>Filter by Date</h3>", unsafe_allow_html=True)
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])  # Ensure 'Date' column is datetime
            start_date = st.sidebar.date_input("Start Date", data['Date'].min())
            end_date = st.sidebar.date_input("End Date", data['Date'].max())
            data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]
        else:
            st.sidebar.warning("Date filtering requires a 'Date' column in the dataset.")

        # Multi-column filters
        st.sidebar.markdown("<h3 style='color: #FF7F50;'>Multiple Filters</h3>", unsafe_allow_html=True)
        filter_columns = st.sidebar.multiselect("Select Columns to Filter By", options=data.columns)

        # Apply filters for selected columns
        for column in filter_columns:
            unique_values = data[column].unique()
            selected_values = st.sidebar.multiselect(f"Select {column} values", unique_values, default=unique_values)
            data = data[data[column].isin(selected_values)]

        # Visualization type selection and plot generation
        st.markdown("<h4 style='color: #FF7F50;'>Visualization Results</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 14px; color: gray;'>Here’s how your selected data looks based on the visualization settings.</p>", unsafe_allow_html=True)

        # Generate plots based on selection
        if visualization_type == "Bar Chart":
            fig = px.bar(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis} - Bar Chart")
            fig.update_traces(textposition="inside", texttemplate="%{y}")

        elif visualization_type == "Line Chart":
            fig = px.line(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis} - Line Chart")

        elif visualization_type == "Pie Chart":
            fig = px.pie(data, names=x_axis, values=y_axis, title=f"{y_axis} Distribution - Pie Chart", hole=0.3)  # Optional: Donut hole
            fig.update_traces(textinfo="label+percent", insidetextorientation="radial")

        elif visualization_type == "Heatmap":
            correlation_matrix = data[[x_axis, y_axis]].corr()
            fig = px.imshow(correlation_matrix, text_auto=True, title=f"Correlation Heatmap: {x_axis} and {y_axis}")

            # Making inside heatmap values **bold**
            fig.update_traces(
                textfont=dict(size=16, color="white", family="Arial white")  # Bold white values inside heatmap
            )

        elif visualization_type == "Boxplot":
            fig = px.box(data, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis} - Boxplot")

        elif visualization_type == "Scatterplot":
            fig = px.scatter(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis} - Scatterplot")
            fig.update_traces(mode="markers+text", textposition="top center", text=data[y_axis])

        # Apply layout customizations
        fig.update_layout(
            title=dict(font=dict(size=20)),  # Bigger title
            xaxis=dict(
                title_font=dict(size=16, color="white", family="Arial white"),  # Bold white X-axis label
                tickfont=dict(size=14, color="white", family="Arial white")  # Bold white X-axis values
            ),
            yaxis=dict(
                title_font=dict(size=16, color="white", family="Arial white"),  # Bold white Y-axis label
                tickfont=dict(size=14, color="white", family="Arial white")  # Bold white Y-axis values
            ),
            legend=dict(
                title_font=dict(size=14, color="white", family="Arial white"), 
                font=dict(size=12, color="white", family="Arial white")  # Bold white legend
            )
        )

        # Update layout for hover interaction
        fig.update_traces(hovertemplate="%{x}: %{y}")

        # Display the interactive plot
        st.plotly_chart(fig)

        # Textual summary based on the displayed visualization
        st.subheader("Textual Summary")
        if visualization_type == "Bar Chart":
            st.write(f"The bar chart shows the relationship between {x_axis} and {y_axis}. High bars indicate higher values for {y_axis}. This visualization is useful for comparing values across categories in {x_axis}.")
        elif visualization_type == "Line Chart":
            st.write(f"The line chart shows the trend of {y_axis} over {x_axis}. Notice any upward or downward trends that could indicate seasonal patterns or other dependencies over time.")
        elif visualization_type == "Pie Chart":
            st.write(f"The pie chart displays the distribution of {y_axis}. Each slice represents the proportion of a category within {y_axis}, providing a sense of the overall distribution.")
        elif visualization_type == "Heatmap":
            st.write(f"The heatmap highlights the correlation between {x_axis} and {y_axis}. Values closer to 1 or -1 indicate a stronger correlation, which can be useful for understanding how one attribute may influence the other.")
        elif visualization_type == "Boxplot":
            st.write(f"The boxplot shows the distribution of {y_axis} across {x_axis} categories. Observe the spread and outliers to understand how values vary across different categories.")
        elif visualization_type == "Scatterplot":
            st.write(f"The scatterplot illustrates the relationship between {x_axis} and {y_axis}. Clusters, slopes, or patterns here might indicate how one variable impacts the other, and outliers are more easily detected.")

    else:
        # Warning message if data is not available
        st.warning("No data available. Please upload a file through the data preview section.")

if __name__ == "__main__":
    pass
