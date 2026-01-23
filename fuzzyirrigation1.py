import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class FuzzyIrrigationSystem:
    """
    Fuzzy Logic System for Agricultural Irrigation
    Inputs: Soil Moisture, Temperature, Humidity
    Output: Water Amount
    """

    def __init__(self):
        self.soil_moisture = 50
        self.temperature = 25
        self.humidity = 50

    # ============ MEMBERSHIP FUNCTIONS ============

    def moisture_dry(self, x):
        """Membership function for dry soil (triangular)"""
        if x <= 30:
            return 1.0
        elif x <= 50:
            return (50 - x) / 20
        else:
            return 0.0

    def moisture_moderate(self, x):
        """Membership function for moderate soil (triangular)"""
        if x <= 30:
            return 0.0
        elif x <= 50:
            return (x - 30) / 20
        elif x <= 70:
            return (70 - x) / 20
        else:
            return 0.0

    def moisture_wet(self, x):
        """Membership function for wet soil (triangular)"""
        if x <= 50:
            return 0.0
        elif x <= 70:
            return (x - 50) / 20
        else:
            return 1.0

    def temp_cold(self, x):
        """Membership function for cold temperature"""
        if x <= 15:
            return 1.0
        elif x <= 25:
            return (25 - x) / 10
        else:
            return 0.0

    def temp_moderate(self, x):
        """Membership function for moderate temperature"""
        if x <= 15:
            return 0.0
        elif x <= 25:
            return (x - 15) / 10
        elif x <= 35:
            return (35 - x) / 10
        else:
            return 0.0

    def temp_hot(self, x):
        """Membership function for hot temperature"""
        if x <= 25:
            return 0.0
        elif x <= 35:
            return (x - 25) / 10
        else:
            return 1.0

    def humidity_low(self, x):
        """Membership function for low humidity"""
        if x <= 30:
            return 1.0
        elif x <= 50:
            return (50 - x) / 20
        else:
            return 0.0

    def humidity_medium(self, x):
        """Membership function for medium humidity"""
        if x <= 30:
            return 0.0
        elif x <= 50:
            return (x - 30) / 20
        elif x <= 70:
            return (70 - x) / 20
        else:
            return 0.0

    def humidity_high(self, x):
        """Membership function for high humidity"""
        if x <= 50:
            return 0.0
        elif x <= 70:
            return (x - 50) / 20
        else:
            return 1.0

    # ============ FUZZY RULES ============

    def apply_fuzzy_rules(self, moisture, temp, humid):
        """
        Apply fuzzy rules to determine water output levels
        Returns: Dictionary with membership values for low, medium, high water
        """
        # Calculate membership values for inputs
        m_dry = self.moisture_dry(moisture)
        m_moderate = self.moisture_moderate(moisture)
        m_wet = self.moisture_wet(moisture)

        t_cold = self.temp_cold(temp)
        t_moderate = self.temp_moderate(temp)
        t_hot = self.temp_hot(temp)

        h_low = self.humidity_low(humid)
        h_medium = self.humidity_medium(humid)
        h_high = self.humidity_high(humid)

        # Initialize output fuzzy sets
        water_low = 0.0
        water_medium = 0.0
        water_high = 0.0

        # Rule 1: If soil is wet, water is low
        water_low = max(water_low, m_wet)

        # Rule 2: If soil is dry AND temp is hot, water is high
        water_high = max(water_high, min(m_dry, t_hot))

        # Rule 3: If soil is dry AND humidity is low, water is high
        water_high = max(water_high, min(m_dry, h_low))

        # Rule 4: If soil is moderate AND temp is moderate, water is medium
        water_medium = max(water_medium, min(m_moderate, t_moderate))

        # Rule 5: If soil is moderate AND humidity is high, water is low
        water_low = max(water_low, min(m_moderate, h_high))

        # Rule 6: If soil is dry AND temp is cold, water is medium
        water_medium = max(water_medium, min(m_dry, t_cold))

        # Rule 7: If humidity is high AND temp is cold, water is low
        water_low = max(water_low, min(h_high, t_cold))

        # Rule 8: If soil is moderate AND temp is hot AND humidity is low, water is high
        water_high = max(water_high, min(min(m_moderate, t_hot), h_low))

        return {
            'low': water_low,
            'medium': water_medium,
            'high': water_high
        }

    # ============ DEFUZZIFICATION ============

    def defuzzify(self, water_levels):
        """
        Centroid defuzzification method
        Converts fuzzy output to crisp value
        """
        # Center points for each fuzzy set
        low_center = 25
        medium_center = 50
        high_center = 75

        # Calculate centroid
        numerator = (water_levels['low'] * low_center +
                     water_levels['medium'] * medium_center +
                     water_levels['high'] * high_center)

        denominator = (water_levels['low'] +
                       water_levels['medium'] +
                       water_levels['high'])

        if denominator == 0:
            return 50  # Default value

        return numerator / denominator

    # ============ COMPUTATION ============

    def compute_water_amount(self, moisture, temp, humid):
        """Main computation method"""
        water_levels = self.apply_fuzzy_rules(moisture, temp, humid)
        water_amount = self.defuzzify(water_levels)
        return water_amount, water_levels

    # ============ VISUALIZATION ============

    def plot_membership_functions(self):
        """Plot all membership functions"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Fuzzy Logic Irrigation System - Membership Functions',
                     fontsize=16, fontweight='bold')

        # Soil Moisture
        x_moisture = np.linspace(0, 100, 200)
        y_dry = [self.moisture_dry(x) for x in x_moisture]
        y_moderate = [self.moisture_moderate(x) for x in x_moisture]
        y_wet = [self.moisture_wet(x) for x in x_moisture]

        axes[0, 0].plot(x_moisture, y_dry, 'r-', label='Dry', linewidth=2)
        axes[0, 0].plot(x_moisture, y_moderate, 'g-',
                        label='Moderate', linewidth=2)
        axes[0, 0].plot(x_moisture, y_wet, 'b-', label='Wet', linewidth=2)
        axes[0, 0].set_xlabel('Soil Moisture (%)')
        axes[0, 0].set_ylabel('Membership Degree')
        axes[0, 0].set_title('Soil Moisture')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim([-0.1, 1.1])

        # Temperature
        x_temp = np.linspace(0, 50, 200)
        y_cold = [self.temp_cold(x) for x in x_temp]
        y_temp_mod = [self.temp_moderate(x) for x in x_temp]
        y_hot = [self.temp_hot(x) for x in x_temp]

        axes[0, 1].plot(x_temp, y_cold, 'c-', label='Cold', linewidth=2)
        axes[0, 1].plot(x_temp, y_temp_mod, 'orange',
                        label='Moderate', linewidth=2)
        axes[0, 1].plot(x_temp, y_hot, 'r-', label='Hot', linewidth=2)
        axes[0, 1].set_xlabel('Temperature (°C)')
        axes[0, 1].set_ylabel('Membership Degree')
        axes[0, 1].set_title('Temperature')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_ylim([-0.1, 1.1])

        # Humidity
        x_humidity = np.linspace(0, 100, 200)
        y_low = [self.humidity_low(x) for x in x_humidity]
        y_medium = [self.humidity_medium(x) for x in x_humidity]
        y_high = [self.humidity_high(x) for x in x_humidity]

        axes[1, 0].plot(x_humidity, y_low, 'r-', label='Low', linewidth=2)
        axes[1, 0].plot(x_humidity, y_medium, 'g-',
                        label='Medium', linewidth=2)
        axes[1, 0].plot(x_humidity, y_high, 'b-', label='High', linewidth=2)
        axes[1, 0].set_xlabel('Humidity (%)')
        axes[1, 0].set_ylabel('Membership Degree')
        axes[1, 0].set_title('Humidity')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_ylim([-0.1, 1.1])

        # Water Output (simplified representation)
        x_water = np.linspace(0, 100, 200)
        # Triangular membership functions for output
        y_water_low = [max(0, min(1, (45-x)/10)) if x <=
                       45 else 0 for x in x_water]
        y_water_med = [max(0, min((x-35)/10, (65-x)/20))
                       if 35 <= x <= 65 else 0 for x in x_water]
        y_water_high = [max(0, min((x-55)/10, 1)) if x >=
                        55 else 0 for x in x_water]

        axes[1, 1].plot(x_water, y_water_low, 'g-', label='Low', linewidth=2)
        axes[1, 1].plot(x_water, y_water_med, 'orange',
                        label='Medium', linewidth=2)
        axes[1, 1].plot(x_water, y_water_high, 'r-', label='High', linewidth=2)
        axes[1, 1].set_xlabel('Water Amount (%)')
        axes[1, 1].set_ylabel('Membership Degree')
        axes[1, 1].set_title('Water Output')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_ylim([-0.1, 1.1])

        plt.tight_layout()
        plt.show()

    def interactive_demo(self):
        """Create interactive demo with sliders"""
        fig, ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(left=0.1, bottom=0.35)

        # Initial computation
        water_amount, water_levels = self.compute_water_amount(
            self.soil_moisture, self.temperature, self.humidity
        )

        # Text display
        result_text = ax.text(0.5, 0.7, '', transform=ax.transAxes,
                              fontsize=14, ha='center', va='center',
                              bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

        info_text = ax.text(0.5, 0.3, '', transform=ax.transAxes,
                            fontsize=11, ha='center', va='center',
                            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Create sliders
        ax_moisture = plt.axes([0.15, 0.20, 0.7, 0.03])
        ax_temp = plt.axes([0.15, 0.15, 0.7, 0.03])
        ax_humid = plt.axes([0.15, 0.10, 0.7, 0.03])

        slider_moisture = Slider(ax_moisture, 'Soil Moisture (%)', 0, 100,
                                 valinit=self.soil_moisture, valstep=1)
        slider_temp = Slider(ax_temp, 'Temperature (°C)', 0, 50,
                             valinit=self.temperature, valstep=1)
        slider_humid = Slider(ax_humid, 'Humidity (%)', 0, 100,
                              valinit=self.humidity, valstep=1)

        def update(val):
            moisture = slider_moisture.val
            temp = slider_temp.val
            humid = slider_humid.val

            water_amount, water_levels = self.compute_water_amount(
                moisture, temp, humid)

            # Determine category
            if water_amount < 40:
                category = "LOW WATER"
                color = 'lightgreen'
            elif water_amount < 60:
                category = "MEDIUM WATER"
                color = 'lightyellow'
            else:
                category = "HIGH WATER"
                color = 'lightcoral'

            result_text.set_text(
                f'RECOMMENDED WATER AMOUNT\n\n'
                f'{water_amount:.1f}%\n\n'
                f'{category}'
            )
            result_text.get_bbox_patch().set_facecolor(color)

            info_text.set_text(
                f'Fuzzy Output Levels:\n'
                f'Low: {water_levels["low"]*100:.0f}%  |  '
                f'Medium: {water_levels["medium"]*100:.0f}%  |  '
                f'High: {water_levels["high"]*100:.0f}%\n\n'
                f'Current Inputs:\n'
                f'Moisture: {moisture:.0f}%  |  Temp: {temp:.0f}°C  |  Humidity: {humid:.0f}%'
            )

            fig.canvas.draw_idle()

        slider_moisture.on_changed(update)
        slider_temp.on_changed(update)
        slider_humid.on_changed(update)

        # Initial update
        update(None)

        plt.show()


# ============ MAIN EXECUTION ============

def main():
    """Main function to run the fuzzy irrigation system"""
    print("=" * 60)
    print("FUZZY LOGIC IRRIGATION SYSTEM")
    print("=" * 60)

    # Create fuzzy system instance
    fuzzy_system = FuzzyIrrigationSystem()

    # Menu
    while True:
        print("\nChoose an option:")
        print("1. Calculate water amount (single input)")
        print("2. View membership functions")
        print("3. Interactive demo (with sliders)")
        print("4. Run multiple test cases")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            # Single calculation
            print("\n" + "-" * 40)
            try:
                moisture = float(input("Enter soil moisture (0-100%): "))
                temp = float(input("Enter temperature (0-50°C): "))
                humid = float(input("Enter humidity (0-100%): "))

                water_amount, water_levels = fuzzy_system.compute_water_amount(
                    moisture, temp, humid
                )

                print("\n" + "=" * 40)
                print(f"RECOMMENDED WATER AMOUNT: {water_amount:.2f}%")
                print("=" * 40)
                print(f"\nFuzzy Output Levels:")
                print(f"  Low:    {water_levels['low']*100:.1f}%")
                print(f"  Medium: {water_levels['medium']*100:.1f}%")
                print(f"  High:   {water_levels['high']*100:.1f}%")

                if water_amount < 40:
                    print("\nCategory: LOW WATER")
                elif water_amount < 60:
                    print("\nCategory: MEDIUM WATER")
                else:
                    print("\nCategory: HIGH WATER")

            except ValueError:
                print("Invalid input! Please enter numeric values.")

        elif choice == '2':
            # Plot membership functions
            print("\nDisplaying membership functions...")
            fuzzy_system.plot_membership_functions()

        elif choice == '3':
            # Interactive demo
            print("\nLaunching interactive demo...")
            print("Use the sliders to adjust inputs and see real-time results!")
            fuzzy_system.interactive_demo()

        elif choice == '4':
            # Test cases
            print("\n" + "=" * 60)
            print("RUNNING TEST CASES")
            print("=" * 60)

            test_cases = [
                (20, 35, 30),   # Very dry, hot, low humidity
                (80, 15, 80),   # Very wet, cold, high humidity
                (50, 25, 50),   # All moderate
                (30, 30, 40),   # Boundary case
                (60, 20, 60),   # Moderate-wet, cool, medium-high humidity
            ]

            for i, (m, t, h) in enumerate(test_cases, 1):
                water_amount, water_levels = fuzzy_system.compute_water_amount(
                    m, t, h)
                print(f"\nTest {i}: Moisture={m}%, Temp={t}°C, Humidity={h}%")
                print(f"  → Water Amount: {water_amount:.2f}%")
                print(f"     (Low: {water_levels['low']:.2f}, "
                      f"Medium: {water_levels['medium']:.2f}, "
                      f"High: {water_levels['high']:.2f})")

        elif choice == '5':
            print("\nExiting... Thank you!")
            break

        else:
            print("\nInvalid choice! Please enter 1-5.")


if __name__ == "__main__":
    main()
