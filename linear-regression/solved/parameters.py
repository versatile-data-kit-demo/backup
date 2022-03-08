parameters = {
    'charge_level_start': dict(
        label="Select Value for the Starting Charge Level",
        value=80,
        max_value=100,
        min_value=1
    ),
    'temperature_start_c': dict(
        label="What's the Temperature Outside? In Celsius Please!",
        value=20,
        max_value=50,
        min_value=-50
    ),
    'distance_km': dict(
        label="How Many Kilometers Are We Going to Drive?",
        value=50,
        max_value=1000,
        min_value=1
    ),
    'average_speed_kmh': dict(
        label="What's the Average Speed We Expect (in Kilometers per Hour)?",
        value=60,
        max_value=300,
        min_value=1
    ),
    'average_consumption_kwhkm': dict(
        label="Any Guesses on the Average Consumption (in kwhkm)?",
        value=15,
        max_value=50,
        min_value=1
    ),
    'heated_seats': dict(
        label="Do We Plan on Using the Heated Seats? (1 = Yes, 0 = No)",
        value=1,
        min_value=0,
        max_value=1
    ),
    'eco_mode': dict(
        label="Do We Plan on Using the Eco Mode? (1 = Yes, 0 = No)",
        value=1,
        min_value=0,
        max_value=1
    )
}
