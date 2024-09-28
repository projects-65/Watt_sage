import streamlit as st
# Define the Streamlit app
st.title("Energy Consumption Estimator")

# Input for appliances
st.header("Enter Your Appliance Details")

# Define a dictionary for appliance types and their power rating ranges
appliance_ranges = {
    "Fridge": (100, 800),
    "Ceiling Fan": (70, 80),
    "TV": (50, 200),
    "Inverter": (50, 50000),
    "Aquaguard": (25, 60),
    "WiFi": (2, 20),
    "Geyser": (50, 5000),
    "Tubelight": (30, 50),
    "Light Bulb": (2, 100),
    "Mixer": (500, 750),
    "Cooler": (100, 200),
    "Electric Vehicle": (22000, 200000),  # kW to W
    "Table Fan": (30, 60),
    "Electric Stove": (1000, 3000),
    "Mobile/Tablet": (5, 15),
    "Mosquito Bat": (10, 10),
    "Mosquito Repellent": (5, 5),
    "Immersion Rod": (1000, 1500),
    "Extension Board": (1250, 3500),
    "Laptop": (30, 70),
    "Computer": (200, 500),
    "Air Conditioner": (3000, 3500),
    "Washing Machine": (400, 2500),
    "Clothes Dryer": (1500, 5000),
    "Dishwasher": (1200, 2400),
    "Iron Box": (750, 1000),
    "Hair Straightener": (85, 175),
    "Electric Oven": (2000, 5000),
    "Room Heater": (800, 1500),
    "Water Pump": (250, 500),
    "Chimney": (150, 300),
    "Kettle": (1200, 1500)
}

# Create a list to store appliance details
appliance_details = []

# Input for multiple appliances
num_appliances = st.number_input("Enter the number of different appliance types", min_value=1, step=1)

for i in range(num_appliances):
    with st.expander(f"Appliance {i + 1}"):
        appliance_name = st.selectbox(f'Select Appliance Type {i + 1}', list(appliance_ranges.keys()), key=f'appliance_{i}')
        
        # Get power rating range for the selected appliance
        min_power, max_power = appliance_ranges[appliance_name]
        power_rating = st.number_input(f'Power Rating (W) for {appliance_name} (Choose between {min_power} - {max_power})', 
                                       min_value=min_power, max_value=max_power, key=f'power_{i}')
                                       
        num_units = st.number_input(f'Number of {appliance_name}(s)', min_value=0, step=1, key=f'units_{i}')
        usage_hours = st.number_input(f'Usage Hours per Day for {appliance_name}(s)', min_value=0.0, key=f'hours_{i}')
        
        if num_units > 0 and usage_hours > 0 and power_rating > 0:
            appliance_details.append((appliance_name, power_rating, num_units, usage_hours))

# Input for electricity bill and household information
st.header("Monthly Electricity Bill Details (INR)")
monthly_bill = st.number_input("Enter your monthly electricity bill (INR)", min_value=0.0)
number_of_people = st.number_input("Number of people in the household", min_value=1)

# Calculate button
if st.button("Calculate Consumption"):
    total_consumption = 0
    consumption_details = []

    for appliance_name, power, num, hours in appliance_details:
        appliance_consumption = (power * num * hours) / 1000  # Convert to kWh
        total_consumption += appliance_consumption
        consumption_details.append((appliance_name, appliance_consumption))

    st.success(f'Total Estimated Energy Consumption: {total_consumption:.2f} kWh')

    # Calculate estimated daily usage from the bill
    average_cost_per_kWh = 8.0  # Average cost per kWh in INR (update as needed)
    estimated_daily_usage = (monthly_bill / average_cost_per_kWh) / 30  # Convert to daily usage

    st.write(f"Estimated Daily Usage Based on Bill: {estimated_daily_usage:.2f} kWh")

    # Categorize consumption
    THRESHOLD = 30.0  # Set as a float, e.g., 30 kWh
    high_consumption_appliances = [(appliance, consumption) for appliance, consumption in consumption_details if consumption > THRESHOLD]

    if total_consumption > THRESHOLD:
        st.warning("This is considered high energy consumption.")
        
        # Show which appliances consumed more energy
        if high_consumption_appliances:
            st.write("Appliances contributing to high energy consumption:")
            for appliance, consumption in high_consumption_appliances:
                st.write(f"- {appliance}: {consumption:.2f} kWh")

        st.info("High energy consumption may indicate inefficiencies. Consider the following precautions:")
        st.write("- Turn off appliances when not in use.")
        st.write("- Use energy-efficient appliances.")
        st.write("- Monitor and adjust usage patterns.")
    else:
        st.success("Your energy consumption is within a good range.")

    # Provide a sustainability quote with styling
    st.markdown("<h3 style='color: green; font-weight: bold;'>Sustainability Tip:</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: blue; font-weight: bold;'>Every small action counts! Save energy, save the planet.</p>", unsafe_allow_html=True)

# Run the app
if __name__ == '__main__':
    st.write("Streamlit app is running...")
