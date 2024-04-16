import numpy as np

#Use the directory wherein the titanic_mod file is saved locally to open up file
with open('titanic_mod.csv', 'r', encoding='utf-8-sig') as file:    
    array = np.genfromtxt(file, delimiter=',', dtype=str, skip_header=1)
    
def user():
    print("""Main Menu
1. Compute Correlation
2. Ranked List of 20 Oldest Survivors by Passenger Class Number
3. Ranked List of 20 Female Survivors by Highest Non-self Family Member Onboard Count and then by Highest Fare
0. Exit""")
    print()
    while True:
        option_first = input("Enter your option (0 to exit): ")
        print()
        
        try:
            option = int(option_first)
            if option == 1:
                print("""List of header names for calculating correlation
0 passenger_id
1 survived
2 pclass
3 gender
4 age
5 sibsp
6 parch
7 fare""")
                print()
                      
                option_cor1 = int(input("Enter the number for the first quantity:"))
                option_cor2 = int(input("Enter the number for the second quantity:"))

                correlation_dict = {
                    0: "passenger_id",
                    1: "survived",
                    2: "pclass",
                    3: "gender",
                    4: "age",
                    5: "sibsp",
                    6: "parch",
                    7: "fare"
                }
                
                array_numeric = np.array(array, dtype=float)
                
                corrcoef = np.corrcoef(array_numeric[:, option_cor1], array_numeric[:, option_cor2]) 
                print()
                print(f"The correlation between {correlation_dict[option_cor1]} and {correlation_dict[option_cor2]} is {corrcoef[0, 1]:.3f}")

            elif option == 2:
                print("Enter the passenger class number (1 to 3):")
                print()
                pclass = int(input())

                survivors_class = array[(array[:, 2] == str(pclass)) & (array[:, 1] == '1')]
                
                survivors_class[:, 4] = survivors_class[:, 4].astype(int)

                survivors_class[:, 7] = np.round(survivors_class[:, 7].astype(float), 2)

                oldest_survivors = survivors_class[np.argsort(-survivors_class[:, 4].astype(int))][:20]

                max_widths = [max(len(str(header[i])), max(len(str(value)) for value in column)) for i, column in enumerate(oldest_survivors.T)]
                
                print("List of the 20 Oldest Survivors for Passenger Cabin Class Number", pclass)
                print()

                header_str = ' '.join(header[i].ljust(max_widths[i] + 6) for i in range(len(header)))  
                print(header_str)
                
                for row in oldest_survivors:
                    row_str = ' '.join(str(row[i]).ljust(max_widths[i] + 6) for i in range(len(row)))  
                    print(row_str)
                                        
            elif option == 3:
                
                calculate_ns_family_members = lambda row: int(row[5]) + int(row[6])

                family_members_column = np.apply_along_axis(calculate_ns_family_members, axis=1, arr=array)

                family_members_column = np.reshape(family_members_column, (-1, 1))

                array_with_ns_family_members = np.append(array, family_members_column, axis=1)

                female_survivors_array = array_with_ns_family_members[(array_with_ns_family_members[:, 1] == '1') & (array_with_ns_family_members[:, 3] == '0')]


                sorted_indices = np.lexsort((-female_survivors_array[:, 7].astype(float), -female_survivors_array[:, -1].astype(int)))

                female_survivors_sorted = female_survivors_array[sorted_indices][:20]

                new_header = header + ['sibsp_parch']
                
                final_array = np.vstack((new_header, female_survivors_sorted))
                
                print("List of 20 Female Survivors by Highest Non-self Family Member Onboard Count, and then by Highest Fare, in descending order")
                print()

                print(''.join(f'{header.ljust(15)}' for header in final_array[0]))  
                for row in final_array[1:]:
                    row_formatted = [value if i != 7 else f"{float(value):.2f}" for i, value in enumerate(row)]  
                    print(''.join(f"{value.ljust(15)}" for value in row_formatted))  

            elif option == 0:
                print("Exiting program.")
                break
                
            else:
                print("Invalid option. Please enter a number from 0 to 3.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

user()
