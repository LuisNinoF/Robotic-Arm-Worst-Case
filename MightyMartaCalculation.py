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
## Payload Contribution to total torque
payload_subtotal_torque_D148 = static_torque_load_Payload + dynamic_torque_load_Payload
print(f"Payload Contribution to Total Torque on D148: {payload_subtotal_torque_D148:.2f} Nm")
payload_contribution = payload_subtotal_torque_D148 / total_torque_D148 * 100
print(f"Payload Contribution Percentage to Total Torque on D148: {payload_contribution:.2f} %")

## D86 Contribution to total torque
d86_subtotal_torque_D148 = 2 * (static_torque_load_D86 + dynamic_torque_load_D86)
print(f"D86 Contribution to Total Torque on D148: {d86_subtotal_torque_D148:.2f} Nm")
d86_contribution = d86_subtotal_torque_D148 / total_torque_D148 * 100
print(f"D86 Contribution Percentage to Total Torque on D148: {d86_contribution:.2f} %")

print(f"End Code")