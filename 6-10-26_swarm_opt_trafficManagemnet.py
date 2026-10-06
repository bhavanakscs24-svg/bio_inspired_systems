import numpy as np
import random


def traffic_delay_objective(green_times):
    """
    Simulates the total intersection vehicle delay.
    In a real system, this would interface with a simulator like SUMO or an explicit queue model.
    Here, we use a mathematical proxy where specific traffic volumes require an ideal split.
    """
    ideal_split = np.array([45, 25, 35, 15]) 
    
    base_delay = np.sum((green_times - ideal_split) ** 2)
    
    target_cycle = 120
    cycle_penalty = abs(np.sum(green_times) - target_cycle) * 50
    
    return base_delay + cycle_penalty

num_particles = 30
num_phases = 4          
max_iter = 100
min_green = 10          
max_green = 80          


w = 0.5   
c1 = 1.5  
c2 = 1.5  


particle_position = np.zeros((num_particles, num_phases))
for i in range(num_particles):

    shares = np.random.dirichlet(np.ones(num_phases))
    particle_position[i] = min_green + shares * (120 - num_phases * min_green)

particle_velocity = np.random.uniform(-2, 2, (num_particles, num_phases))


personal_best_position = np.copy(particle_position)
personal_best_score = np.array([traffic_delay_objective(p) for p in particle_position])

global_best_index = np.argmin(personal_best_score)
global_best_position = np.copy(personal_best_position[global_best_index])
global_best_score = personal_best_score[global_best_index]


for iteration in range(max_iter):
    for i in range(num_particles):
        r1, r2 = random.random(), random.random()
        
        cognitive_velocity = c1 * r1 * (personal_best_position[i] - particle_position[i])
        social_velocity = c2 * r2 * (global_best_position - particle_position[i])
        particle_velocity[i] = w * particle_velocity[i] + cognitive_velocity + social_velocity
        
        particle_position[i] += particle_velocity[i]
        
        particle_position[i] = np.clip(particle_position[i], min_green, max_green)
        
        current_score = traffic_delay_objective(particle_position[i])
        
        if current_score < personal_best_score[i]:
            personal_best_score[i] = current_score
            personal_best_position[i] = np.copy(particle_position[i])
            
            if current_score < global_best_score:
                global_best_score = current_score
                global_best_position = np.copy(particle_position[i])

print("--- Optimization Completed ---")
print(f"Minimum Found Delay Score: {global_best_score:.4f}")
print("Optimal Green Time Allocation (Seconds):")
for phase, duration in enumerate(global_best_position, start=1):
    print(f"  Phase {phase}: {duration:.2f} seconds")
print(f"Total Allocated Cycle Time: {np.sum(global_best_position):.2f} seconds")
