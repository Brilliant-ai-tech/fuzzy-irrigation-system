import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

class AdvancedFuzzyIrrigationSystem:
    """
    Advanced Fuzzy Logic System for Agricultural Irrigation
    Inputs: Soil Moisture, Temperature, Humidity, Plant Type
    Output: Exact Water Amount in Liters per Square Meter
    """
    
    def __init__(self):
        self.soil_moisture = 50
        self.temperature = 25
        self.humidity = 50
        self.plant_type = "tea"
        
        # Plant water requirements (liters per m² per day under optimal conditions)
        self.plant_profiles = {
            "rice": {
                "name": "Rice (High Water)",
                "base_water": 15.0,  # liters/m²/day
                "description": "Water-intensive crop requiring flooded or very moist conditions",
                "optimal_moisture": 80,
                "tolerance": "low"
            },
            "tea": {
                "name": "Tea (Medium Water)",
                "base_water": 8.0,   # liters/m²/day
                "description": "Moderate water needs with good drainage",
                "optimal_moisture": 60,
                "tolerance": "medium"
            },
            "cactus": {
                "name": "Cactus (Low Water)",
                "base_water": 2.0,   # liters/m²/day
                "description": "Drought-tolerant, requires minimal water",
                "optimal_moisture": 30,
                "tolerance": "high"
            }
        }
    
    # ============ MEMBERSHIP FUNCTIONS ============
    
    def moisture_dry(self, x):
        """Membership function for dry soil"""
        if x <= 30:
            return 1.0
        elif x <= 50:
            return (50 - x) / 20
        else:
            return 0.0
    
    def moisture_moderate(self, x):
        """Membership function for moderate soil"""
        if x <= 30:
            return 0.0
        elif x <= 50:
            return (x - 30) / 20
        elif x <= 70:
            return (70 - x) / 20
        else:
            return 0.0
    
    def moisture_wet(self, x):
        """Membership function for wet soil"""
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
        
        # Rule 9: If soil is dry AND humidity is medium, water is high
        water_high = max(water_high, min(m_dry, h_medium))
        
        # Rule 10: If soil is wet AND temp is hot, water is medium (evaporation)
        water_medium = max(water_medium, min(m_wet, t_hot))
        
        return {
            'low': water_low,
            'medium': water_medium,
            'high': water_high
        }
    
    # ============ DEFUZZIFICATION ============
    
    def defuzzify(self, water_levels):
        """
        Centroid defuzzification method
        Converts fuzzy output to crisp percentage (0-100%)
        """
        low_center = 25
        medium_center = 50
        high_center = 75
        
        numerator = (water_levels['low'] * low_center + 
                    water_levels['medium'] * medium_center + 
                    water_levels['high'] * high_center)
        
        denominator = (water_levels['low'] + 
                      water_levels['medium'] + 
                      water_levels['high'])
        
        if denominator == 0:
            return 50
        
        return numerator / denominator
    
    # ============ PLANT-SPECIFIC CALCULATION ============
    
    def calculate_exact_water(self, moisture, temp, humid, plant_type):
        """
        Calculate exact water amount in liters per square meter
        based on fuzzy logic output and plant requirements
        """
        # Get fuzzy logic percentage (0-100%)
        water_levels = self.apply_fuzzy_rules(moisture, temp, humid)
        fuzzy_percentage = self.defuzzify(water_levels)
        
        # Get plant profile
        plant = self.plant_profiles[plant_type]
        base_water = plant["base_water"]
        
        # Convert fuzzy percentage to multiplier (0.0 to 1.5)
        # Low water (0-40%) -> 0.0 to 0.6 multiplier
        # Medium water (40-60%) -> 0.6 to 1.0 multiplier  
        # High water (60-100%) -> 1.0 to 1.5 multiplier
        
        if fuzzy_percentage < 40:
            multiplier = fuzzy_percentage / 40 * 0.6
        elif fuzzy_percentage < 60:
            multiplier = 0.6 + (fuzzy_percentage - 40) / 20 * 0.4
        else:
            multiplier = 1.0 + (fuzzy_percentage - 60) / 40 * 0.5
        
        # Calculate exact water amount
        exact_water = base_water * multiplier
        
        return {
            'liters_per_m2': round(exact_water, 2),
            'fuzzy_percentage': round(fuzzy_percentage, 1),
            'water_levels': water_levels,
            'plant_name': plant["name"],
            'base_requirement': base_water,
            'multiplier': round(multiplier, 2)
        }
    
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
        axes[0, 0].plot(x_moisture, y_moderate, 'g-', label='Moderate', linewidth=2)
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
        axes[0, 1].plot(x_temp, y_temp_mod, 'orange', label='Moderate', linewidth=2)
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
        axes[1, 0].plot(x_humidity, y_medium, 'g-', label='Medium', linewidth=2)
        axes[1, 0].plot(x_humidity, y_high, 'b-', label='High', linewidth=2)
        axes[1, 0].set_xlabel('Humidity (%)')
        axes[1, 0].set_ylabel('Membership Degree')
        axes[1, 0].set_title('Humidity')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_ylim([-0.1, 1.1])
        
        # Water Output
        x_water = np.linspace(0, 100, 200)
        y_water_low = [max(0, min(1, (45-x)/10)) if x <= 45 else 0 for x in x_water]
        y_water_med = [max(0, min((x-35)/10, (65-x)/20)) if 35 <= x <= 65 else 0 for x in x_water]
        y_water_high = [max(0, min((x-55)/10, 1)) if x >= 55 else 0 for x in x_water]
        
        axes[1, 1].plot(x_water, y_water_low, 'g-', label='Low', linewidth=2)
        axes[1, 1].plot(x_water, y_water_med, 'orange', label='Medium', linewidth=2)
        axes[1, 1].plot(x_water, y_water_high, 'r-', label='High', linewidth=2)
        axes[1, 1].set_xlabel('Water Amount (%)')
        axes[1, 1].set_ylabel('Membership Degree')
        axes[1, 1].set_title('Water Output')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_ylim([-0.1, 1.1])
        
        plt.tight_layout()
        plt.show()
    
    def plot_plant_comparison(self):
        """Show water requirements comparison for different plants"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Test conditions
        conditions = [
            (30, 35, 25, "Dry, Hot, Low Humidity"),
            (50, 25, 50, "Moderate All"),
            (70, 15, 75, "Wet, Cold, High Humidity"),
        ]
        
        plants = ["rice", "tea", "cactus"]
        colors = ['#3498db', '#2ecc71', '#e74c3c']
        
        # Bar chart comparison
        x_pos = np.arange(len(conditions))
        width = 0.25
        
        for i, plant in enumerate(plants):
            water_amounts = []
            for moisture, temp, humid, _ in conditions:
                result = self.calculate_exact_water(moisture, temp, humid, plant)
                water_amounts.append(result['liters_per_m2'])
            
            ax1.bar(x_pos + i*width, water_amounts, width, 
                   label=self.plant_profiles[plant]["name"], 
                   color=colors[i], alpha=0.8)
        
        ax1.set_xlabel('Conditions', fontweight='bold')
        ax1.set_ylabel('Water (Liters/m²)', fontweight='bold')
        ax1.set_title('Water Requirements Comparison', fontsize=14, fontweight='bold')
        ax1.set_xticks(x_pos + width)
        ax1.set_xticklabels([cond[3] for cond in conditions], rotation=15, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Base requirements
        base_waters = [self.plant_profiles[p]["base_water"] for p in plants]
        plant_names = [self.plant_profiles[p]["name"] for p in plants]
        
        ax2.barh(plant_names, base_waters, color=colors, alpha=0.8)
        ax2.set_xlabel('Base Water Requirement (Liters/m²/day)', fontweight='bold')
        ax2.set_title('Base Daily Water Requirements', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        for i, v in enumerate(base_waters):
            ax2.text(v + 0.3, i, f'{v} L', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def interactive_demo(self):
        """Create interactive demo with sliders and plant selection"""
        fig = plt.figure(figsize=(12, 9))
        ax_main = plt.subplot2grid((3, 2), (0, 0), colspan=2, rowspan=2)
        ax_radio = plt.subplot2grid((3, 2), (2, 0))
        ax_info = plt.subplot2grid((3, 2), (2, 1))
        
        plt.subplots_adjust(left=0.1, bottom=0.35, right=0.95, top=0.95, hspace=0.4)
        
        # Main display
        result_text = ax_main.text(0.5, 0.65, '', transform=ax_main.transAxes, 
                                  fontsize=13, ha='center', va='center',
                                  bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
        
        detail_text = ax_main.text(0.5, 0.3, '', transform=ax_main.transAxes, 
                                  fontsize=10, ha='center', va='center',
                                  bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
        
        ax_main.set_xlim(0, 1)
        ax_main.set_ylim(0, 1)
        ax_main.axis('off')
        ax_main.set_title('Advanced Fuzzy Irrigation System', fontsize=16, fontweight='bold', pad=20)
        
        # Plant info display
        ax_info.axis('off')
        
        # Radio buttons for plant selection
        radio = RadioButtons(ax_radio, ('Rice (High Water)', 'Tea (Medium Water)', 'Cactus (Low Water)'))
        
        # Sliders
        ax_moisture = plt.axes([0.15, 0.20, 0.7, 0.03])
        ax_temp = plt.axes([0.15, 0.15, 0.7, 0.03])
        ax_humid = plt.axes([0.15, 0.10, 0.7, 0.03])
        
        slider_moisture = Slider(ax_moisture, 'Soil Moisture (%)', 0, 100, 
                                valinit=self.soil_moisture, valstep=1)
        slider_temp = Slider(ax_temp, 'Temperature (°C)', 0, 50, 
                           valinit=self.temperature, valstep=1)
        slider_humid = Slider(ax_humid, 'Humidity (%)', 0, 100, 
                            valinit=self.humidity, valstep=1)
        
        def get_plant_key(label):
            if 'Rice' in label:
                return 'rice'
            elif 'Tea' in label:
                return 'tea'
            else:
                return 'cactus'
        
        def update(val):
            moisture = slider_moisture.val
            temp = slider_temp.val
            humid = slider_humid.val
            plant_key = get_plant_key(radio.value_selected)
            
            result = self.calculate_exact_water(moisture, temp, humid, plant_key)
            plant = self.plant_profiles[plant_key]
            
            # Determine category
            fuzzy_pct = result['fuzzy_percentage']
            if fuzzy_pct < 40:
                category = "LOW WATER"
                color = 'lightgreen'
            elif fuzzy_pct < 60:
                category = "MEDIUM WATER"
                color = 'lightyellow'
            else:
                category = "HIGH WATER"
                color = 'lightcoral'
            
            # Main result
            result_text.set_text(
                f'🌱 {result["plant_name"]}\n\n'
                f'💧 APPLY: {result["liters_per_m2"]} Liters/m²\n\n'
                f'{category} ({fuzzy_pct}%)'
            )
            result_text.get_bbox_patch().set_facecolor(color)
            
            # Details
            detail_text.set_text(
                f'Fuzzy Levels: Low={result["water_levels"]["low"]*100:.0f}% | '
                f'Med={result["water_levels"]["medium"]*100:.0f}% | '
                f'High={result["water_levels"]["high"]*100:.0f}%\n'
                f'Base Requirement: {result["base_requirement"]} L/m²/day | '
                f'Multiplier: {result["multiplier"]}x\n\n'
                f'Current: Moisture={moisture:.0f}% | Temp={temp:.0f}°C | Humidity={humid:.0f}%'
            )
            
            # Plant info
            ax_info.clear()
            ax_info.axis('off')
            info_str = (
                f'{plant["name"]}\n\n'
                f'{plant["description"]}\n\n'
                f'Base: {plant["base_water"]} L/m²/day\n'
                f'Optimal Moisture: {plant["optimal_moisture"]}%\n'
                f'Drought Tolerance: {plant["tolerance"].title()}'
            )
            ax_info.text(0.5, 0.5, info_str, transform=ax_info.transAxes,
                        fontsize=9, ha='center', va='center',
                        bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.7))
            
            fig.canvas.draw_idle()
        
        slider_moisture.on_changed(update)
        slider_temp.on_changed(update)
        slider_humid.on_changed(update)
        radio.on_clicked(update)
        
        # Initial update
        update(None)
        
        plt.show()


# ============ MAIN EXECUTION ============

def main():
    """Main function to run the advanced fuzzy irrigation system"""
    print("=" * 70)
    print("ADVANCED FUZZY LOGIC IRRIGATION SYSTEM")
    print("Plant-Specific Water Calculation (Liters per Square Meter)")
    print("=" * 70)
    
    fuzzy_system = AdvancedFuzzyIrrigationSystem()
    
    while True:
        print("\n" + "=" * 70)
        print("MAIN MENU")
        print("=" * 70)
        print("1. Calculate exact water amount for specific plant")
        print("2. Compare water needs across all plants")
        print("3. View membership functions")
        print("4. Interactive demo (with sliders)")
        print("5. Run test scenarios")
        print("6. View plant profiles")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            # Single calculation
            print("\n" + "-" * 70)
            print("SELECT PLANT TYPE:")
            print("1. Rice (High Water Requirement)")
            print("2. Tea (Medium Water Requirement)")
            print("3. Cactus (Low Water Requirement)")
            
            plant_choice = input("Enter plant number (1-3): ")
            plant_map = {'1': 'rice', '2': 'tea', '3': 'cactus'}
            
            if plant_choice not in plant_map:
                print("Invalid choice!")
                continue
            
            plant_type = plant_map[plant_choice]
            
            try:
                moisture = float(input("Enter soil moisture (0-100%): "))
                temp = float(input("Enter temperature (0-50°C): "))
                humid = float(input("Enter humidity (0-100%): "))
                area = float(input("Enter field area in square meters (m²): "))
                
                result = fuzzy_system.calculate_exact_water(moisture, temp, humid, plant_type)
                total_water = result['liters_per_m2'] * area
                
                print("\n" + "=" * 70)
                print(f"🌱 PLANT: {result['plant_name']}")
                print("=" * 70)
                print(f"💧 WATER REQUIRED: {result['liters_per_m2']} Liters per m²")
                print(f"📏 FIELD AREA: {area} m²")
                print(f"🚰 TOTAL WATER NEEDED: {total_water:.2f} Liters ({total_water/1000:.2f} m³)")
                print("=" * 70)
                print(f"\nFuzzy Logic Analysis:")
                print(f"  Fuzzy Percentage: {result['fuzzy_percentage']}%")
                print(f"  Low Water Level: {result['water_levels']['low']*100:.1f}%")
                print(f"  Medium Water Level: {result['water_levels']['medium']*100:.1f}%")
                print(f"  High Water Level: {result['water_levels']['high']*100:.1f}%")
                print(f"\nPlant-Specific Calculation:")
                print(f"  Base Requirement: {result['base_requirement']} L/m²/day")
                print(f"  Condition Multiplier: {result['multiplier']}x")
                print(f"  Final Amount: {result['base_requirement']} × {result['multiplier']} = {result['liters_per_m2']} L/m²")
                
                # Category
                if result['fuzzy_percentage'] < 40:
                    print(f"\n✅ Category: LOW WATER - Minimal irrigation needed")
                elif result['fuzzy_percentage'] < 60:
                    print(f"\n⚠️ Category: MEDIUM WATER - Standard irrigation")
                else:
                    print(f"\n🔴 Category: HIGH WATER - Intensive irrigation required")
                    
            except ValueError:
                print("Invalid input! Please enter numeric values.")
        
        elif choice == '2':
            # Compare plants
            print("\n" + "=" * 70)
            print("PLANT WATER REQUIREMENTS COMPARISON")
            print("=" * 70)
            
            try:
                moisture = float(input("Enter soil moisture (0-100%): "))
                temp = float(input("Enter temperature (0-50°C): "))
                humid = float(input("Enter humidity (0-100%): "))
                
                print("\n" + "-" * 70)
                print(f"Conditions: Moisture={moisture}%, Temp={temp}°C, Humidity={humid}%")
                print("-" * 70)
                
                for plant_key in ['rice', 'tea', 'cactus']:
                    result = fuzzy_system.calculate_exact_water(moisture, temp, humid, plant_key)
                    print(f"\n{result['plant_name']}:")
                    print(f"  Water Required: {result['liters_per_m2']} L/m²")
                    print(f"  Fuzzy %: {result['fuzzy_percentage']}%")
                    print(f"  Multiplier: {result['multiplier']}x")
                
            except ValueError:
                print("Invalid input!")
        
        elif choice == '3':
            # Plot membership functions
            print("\nDisplaying membership functions...")
            fuzzy_system.plot_membership_functions()
        
        elif choice == '4':
            # Interactive demo
            print("\nLaunching interactive demo...")
            print("Select plant type and adjust sliders to see exact water requirements!")
            fuzzy_system.interactive_demo()
        
        elif choice == '5':
            # Test scenarios
            print("\n" + "=" * 70)
            print("RUNNING TEST SCENARIOS")
            print("=" * 70)
            
            scenarios = [
                (25, 38, 20, "Extreme: Very Dry, Very Hot, Very Low Humidity"),
                (50, 25, 50, "Ideal: Moderate All Conditions"),
                (75, 15, 80, "Wet: High Moisture, Cool, High Humidity"),
                (40, 32, 30, "Challenging: Somewhat Dry, Hot, Low Humidity"),
            ]
            
            for moisture, temp, humid, desc in scenarios:
                print(f"\n{'-' * 70}")
                print(f"Scenario: {desc}")
                print(f"Conditions: Moisture={moisture}%, Temp={temp}°C, Humidity={humid}%")
                print(f"{'-' * 70}")
                
                for plant_key in ['rice', 'tea', 'cactus']:
                    result = fuzzy_system.calculate_exact_water(moisture, temp, humid, plant_key)
                    print(f"{result['plant_name']:20} → {result['liters_per_m2']:6.2f} L/m² "
                          f"(Fuzzy: {result['fuzzy_percentage']:5.1f}%)")
        
        elif choice == '6':
            # View plant profiles
            print("\n" + "=" * 70)
            print("PLANT PROFILES")
            print("=" * 70)
            
            for plant_key, plant in fuzzy_system.plant_profiles.items():
                print(f"\n{plant['name']}")
                print("-" * 50)
                print(f"Description: {plant['description']}")
                print(f"Base Water Requirement: {plant['base_water']} Liters/m²/day")
                print(f"Optimal Soil Moisture: {plant['optimal_moisture']}%")
                print(f"Drought Tolerance: {plant['tolerance'].title()}")
            
            print("\n" + "-" * 70)
            print("Visual comparison:")
            fuzzy_system.plot_plant_comparison()
        
        elif choice == '7':
            print("\nExiting... Happy farming! 🌱")
            break
        
        else:
            print("\nInvalid choice! Please enter 1-7.")


if __name__ == "__main__":
    main()