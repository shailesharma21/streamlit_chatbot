import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    if "content" in msg:
        st.chat_message(msg["role"]).write(msg["content"])
    if "chart" in msg:
        st.image(msg["chart"], use_column_width=True)

# Test data
df = pd.DataFrame(
    {"Category": ["A", "B", "C", "A", "B", "C"], "Value": [10, 20, 30, 40, 50, 60]}
)


# Function to generate summary
def generate_summary(data):
    summary = {
        "Total Count": data.shape[0],
        "Value Sum": data["Value"].sum(),
        "Value Mean": data["Value"].mean(),
    }
    return summary


# Function to generate chart
def generate_chart(data):
    plt.bar(data["Category"], data["Value"])
    plt.xlabel("Category")
    plt.ylabel("Value")
    return plt


# Function to convert a matplotlib figure to an image
def fig_to_img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = buf.getvalue()
    return img


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Check user input and generate response
    if prompt.lower() == "summary":
        # Generate summary
        summary = generate_summary(df)
        insight = ""

        for key, value in summary.items():
            insight += f"{key}: {value} \n"

        st.chat_message("assistant").write(insight)
        st.session_state.messages.append({"role": "assistant", "content": insight})

    elif prompt.lower() == "chart":
        # Generate chart
        chart = generate_chart(df)
        st.pyplot(chart)

        # Convert the chart to an image
        image = fig_to_img(chart)

        # Add the chart image to the conversation history
        st.session_state.messages.append({"role": "assistant", "chart": image})

    elif prompt.lower() == "sc":
        summary = generate_summary(df)
        insight = ""

        for key, value in summary.items():
            insight += f"{key}: {value} \n"

        st.chat_message("assistant").write(insight)
        st.markdown("")
        # Generate chart
        chart = generate_chart(df)
        st.pyplot(chart)

        # Convert the chart to an image
        image = fig_to_img(chart)

        st.session_state.messages.append(
            {"role": "assistant", "content": insight, "chart": image}
        )
