import streamlit as st
import hashlib
import datetime

# Define the Block class
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Initialize blockchain with the genesis block
def create_genesis_block():
    return Block(0, str(datetime.datetime.now()), "Genesis Block", "0")

if 'blockchain' not in st.session_state:
    st.session_state.blockchain = [create_genesis_block()]

# Function to add a block to the blockchain
def add_block(data):
    last_block = st.session_state.blockchain[-1]
    new_block = Block(
        index=last_block.index + 1,
        timestamp=str(datetime.datetime.now()),
        data=data,
        previous_hash=last_block.hash
    )
    st.session_state.blockchain.append(new_block)

# Streamlit UI
st.title("🔐 Doctor Appointment Blockchain Booking")

form = st.form("appointment_form")
patient_name = form.text_input("Patient Name")
doctor_name = form.text_input("Doctor Name")
appointment_time = form.date_input("Appointment Date")
appointment_hour = form.time_input("Appointment Time")
submit_button = form.form_submit_button("Book Appointment")

if submit_button:
    appointment_datetime = datetime.datetime.combine(appointment_time, appointment_hour)
    appointment_data = {
        "patient": patient_name,
        "doctor": doctor_name,
        "time": str(appointment_datetime)
    }
    add_block(str(appointment_data))
    st.success("Appointment booked and added to blockchain!")

st.subheader("📂 Current Blockchain:")
for block in st.session_state.blockchain:
    st.write(f"**Block {block.index}:**")
    st.json({
        "Timestamp": block.timestamp,
        "Data": block.data,
        "Previous Hash": block.previous_hash,
        "Hash": block.hash
    })
