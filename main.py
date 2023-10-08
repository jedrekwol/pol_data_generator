from src.pol_data_gen import PolDataGenerator

gen = PolDataGenerator(output='str', seed=42)

# geerate first name
first_name = gen.generate_name(name_type='first', sex='F')
print(first_name)

# generate full personal data
person = gen.generate_person()
print(person)