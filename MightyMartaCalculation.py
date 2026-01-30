### Input data ---------------------------------------------------------------------------------------------

# Constants
GRAVITY = 9.81  # m/s^2
PI = 3.14159 # Pi constant

# Assumptions
stop_time = 1.0 # seconds to stop from max velocity

# Create a class to represent a mechanical component with its specifications
class Component:
    def __init__(self, type, diameter, length, mass, max_torque, max_velocity):
        self.type = type    # string: "Motor", "Link", "Payload"
        self.diameter = diameter  # in meters
        self.length = length  # in meters
        self.mass = mass  # in kilograms
        self.max_torque = max_torque  # in Newton-meters
        self.max_velocity = max_velocity  # in deg/s

## Define components with their specifications
#      Components:   Type,      Diameter (m), Length (m), Mass (kg), Max Torque (Nm), Max Velocity (deg/s)
D148 = Component    ("Motor",   0.148,          0,        5.0,       433,               180)
D116 = Component    ("Motor",   0.116,          0,        4.0,       204,               180)
D86 =  Component    ("Motor",   0.086,          0,        3.0,       70,                230) 
L148 = Component    ("Link",    0.148,          0.670,    4.0,       0,                 0)
I116 = Component    ("Link",    0.116,          0.600,    3.0,       0,                 0)
Payload = Component ("Payload", 0,              0,        11.5,      0,                 0)




### Static Loads ---------------------------------------------------------------------------------------------

## Individual Static Torque Loads
static_torque_load_L148 = L148.mass * GRAVITY * (L148.length / 2)
static_torque_load_D116 = D116.mass * GRAVITY * (L148.length)
static_torque_load_I116 = I116.mass * GRAVITY * (L148.length + I116.length / 2)
static_torque_load_D86 = D86.mass * GRAVITY * (L148.length + I116.length)
static_torque_load_Payload = Payload.mass * GRAVITY * (L148.length + I116.length)

## Total Static Torque Calculation
static_torque_D148 = (static_torque_load_L148 + 
                      2*static_torque_load_D116 + 
                      static_torque_load_I116 + 
                      2*static_torque_load_D86 + 
                      static_torque_load_Payload)

print(f"Static Torque Load on D148: {static_torque_D148:.2f} Nm")




### Dynamic Loads ---------------------------------------------------------------------------------------------

# Angular Acceleration (rad/s^2)
angular_acceleration = (D148.max_velocity / stop_time) * (PI / 180) # rad/s^2

## Individual Moments of Inertia
# moment of inertia    = moment of inertia at center of mass   + moment of inertia due to distance from rotation axis at D148
moment_of_inertia_L148 = (1/12) * L148.mass * (L148.length**2) + L148.mass * ( (L148.length/2) **2 )
moment_of_inertia_D116 =                                         D116.mass * (L148.length ** 2)
moment_of_inertia_I116 = (1/12) * I116.mass * (I116.length**2) + I116.mass * ( (L148.length + I116.length/2) **2 )
moment_of_inertia_D86 =                                          D86.mass * ( (L148.length + I116.length) **2 )
moment_of_inertia_Payload =                                      Payload.mass * ( (L148.length + I116.length) **2 )

## Individual Dynamic Torque Loads
# dynamic torque load = angular acceleration * moment of inertia
dynamic_torque_load_L148 = angular_acceleration * moment_of_inertia_L148
dynamic_torque_load_D116 = angular_acceleration * moment_of_inertia_D116
dynamic_torque_load_I116 = angular_acceleration * moment_of_inertia_I116
dynamic_torque_load_D86 = angular_acceleration * moment_of_inertia_D86        
dynamic_torque_load_Payload = angular_acceleration * moment_of_inertia_Payload

## Total Dynamic Torque Calculation
dynamic_torque_D148 = (dynamic_torque_load_L148 + 
                       2*dynamic_torque_load_D116 + 
                       dynamic_torque_load_I116 + 
                       2*dynamic_torque_load_D86 + 
                       dynamic_torque_load_Payload)

print(f"Dynamic Torque Load on D148: {dynamic_torque_D148:.2f} Nm")




### Total Loads ---------------------------------------------------------------------------------------------
total_torque_D148 = static_torque_D148 + dynamic_torque_D148
print(f"Total Torque Load on D148: {total_torque_D148:.2f} Nm")
print(f"D148 Max Torque: {D148.max_torque} Nm")




### Analysis  -----------------------------------------------------------------------------------------------

## Contribution of each component to total torque on D148 as a dictionary
contribution = {
    "L148":     (static_torque_load_L148 + dynamic_torque_load_L148),
    "D116 x2":  2 * (static_torque_load_D116 + dynamic_torque_load_D116),
    "I116":     (static_torque_load_I116 + dynamic_torque_load_I116),
    "D86 x2" :  2 * (static_torque_load_D86 + dynamic_torque_load_D86),
    "Payload":  (static_torque_load_Payload + dynamic_torque_load_Payload)
}
# Print Contribution (in Nm & percentage) to total torque using contribution and contribution_percentage dictionary
for component, torque_contribution in contribution.items():
    percentage = torque_contribution / total_torque_D148 * 100
    print(f"{component} Contribution to Total Torque on D148: {torque_contribution:.2f} Nm ({percentage:.2f} %)")





### Visualization  -----------------------------------------------------------------------------------------------

# Import visualization library (matplotlib)
import matplotlib.pyplot as plt

# Prepare data to plot
components_plot = list(contribution.keys())
torques_plot = list(contribution.values())
percentages = [f"{v/total_torque_D148*100:.1f}%" for v in torques_plot]

# Plot data
fig, ax = plt.subplots()
bars = ax.barh(components_plot, torques_plot, color='skyblue')
ax.bar_label(bars, labels=[f'{t:.0f} Nm\n({p})' for t,p in zip(torques_plot, percentages)], 
             padding=8, fontsize=11, fontweight='light')
# Format plot
ax.set_xlabel('Torque Contribution (Nm)')
ax.set_title('Torque Contribution of Each Component to D148')
ax.set_xlim(0, max(torques_plot)*1.2)
#ax.set_yticklabels(components_plot, fontweight='bold', fontsize=12)

# Show plot
plt.tight_layout
plt.show()




print(f"End Code")
