from prettytable import PrettyTable
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Define the constants
E = 30000
mu = 0.15
gamma = 24

# Define the possible values for each level
axle_types = ["Single", "Tandem"]
shoulders = ["with concrete shoulders", "without concrete shoulders"]
delta_t_values = [0, 8, 13, 17, 21]
k_values = [40, 80, 150, 300]
h_values = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40]

# Create a dictionary to store P(kN) values based on Axle Type
p_values_dict = {"Single": [80, 120, 160], "Tandem": [160, 200, 240, 300, 320]}


def calculate_S(axle_type, shoulder, k, p, h, l, delta_t):
    if axle_type == "Single":
        if shoulder == "with concrete shoulders":
            if k <= 80:
                return (
                    0.008
                    - 6.12 * gamma * h**2 / (k * l**2)
                    + 2.36 * p * h / (k * l**4)
                    + 0.0266 * delta_t
                )
            elif k <= 150:
                return (
                    0.08
                    - 9.69 * gamma * h**2 / (k * l**2)
                    + 2.09 * p * h / (k * l**4)
                    + 0.0409 * delta_t
                )
            else:
                return (
                    0.042
                    + 3.26 * gamma * h**2 / (k * l**2)
                    + 1.62 * p * h / (k * l**4)
                    + 0.0522 * delta_t
                )
        else:  # without concrete shoulders
            if k <= 80:
                return (
                    -0.149
                    - 2.6 * gamma * h**2 / (k * l**2)
                    + 3.13 * p * h / (k * l**4)
                    + 0.0297 * delta_t
                )
            elif k <= 150:
                return (
                    -0.119
                    - 2.99 * gamma * h**2 / (k * l**2)
                    + 2.78 * p * h / (k * l**4)
                    + 0.0456 * delta_t
                )
            else:
                return (
                    -0.238
                    + 7.02 * gamma * h**2 / (k * l**2)
                    + 2.41 * p * h / (k * l**4)
                    + 0.0585 * delta_t
                )
    else:  # Tandem
        if shoulder == "with concrete shoulders":
            if k <= 80:
                return (
                    -0.188
                    + 0.93 * gamma * h**2 / (k * l**2)
                    + 1.025 * p * h / (k * l**4)
                    + 0.0207 * delta_t
                )
            elif k <= 150:
                return (
                    -0.174
                    + 1.21 * gamma * h**2 / (k * l**2)
                    + 0.87 * p * h / (k * l**4)
                    + 0.0364 * delta_t
                )
            else:
                return (
                    -0.210
                    + 3.88 * gamma * h**2 / (k * l**2)
                    + 0.73 * p * h / (k * l**4)
                    + 0.0506 * delta_t
                )
        else:  # without concrete shoulders
            if k <= 80:
                return (
                    -0.223
                    + 2.73 * gamma * h**2 / (k * l**2)
                    + 1.335 * p * h / (k * l**4)
                    + 0.0229 * delta_t
                )
            elif 80 < k <= 150:
                return (
                    -0.276
                    + 5.78 * gamma * h**2 / (k * l**2)
                    + 1.14 * p * h / (k * l**4)
                    + 0.0404 * delta_t
                )
            else:
                return (
                    -0.3
                    + 9.88 * gamma * h**2 / (k * l**2)
                    + 0.956 * p * h / (k * l**4)
                    + 0.0543 * delta_t
                )


def generateTable():
    # Create a PrettyTable
    table = PrettyTable(
        [
            "Axle Type",
            "Shoulder",
            "P(kN)",
            "del T (C)",
            "k (MPa/m)",
            "h (m)",
            "l (m)",
            "S (kN)",
        ]
    )

    # Nested loops to populate the rows
    for axle_type in axle_types:
        for shoulder in shoulders:
            for p in p_values_dict[axle_type]:
                for delta_t in delta_t_values:
                    for k in k_values:
                        for h in h_values:
                            # Calculate l(m) using the formula
                            l = ((E * h**3) / (12 * k * (1 - mu**2))) ** 0.25

                            # Calculate S(kN) using the function
                            S = calculate_S(axle_type, shoulder, k, p, h, l, delta_t)

                            table.add_row(
                                [
                                    axle_type,
                                    shoulder,
                                    p,
                                    delta_t,
                                    k,
                                    h,
                                    round(l, 4),
                                    round(S, 4),
                                ]
                            )

    return table


# Call the function
result_table = generateTable()

# Print the table
print(result_table)

# Save the table to a CSV file
csv_file_path = "output_table_0.8.13.17.21.csv"
with open(csv_file_path, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(result_table.field_names)
    for row in result_table._rows:
        csv_writer.writerow(row)

print(f"The table has been saved to {csv_file_path}.")


def generatePlots():
    markers = {40: "o", 80: "X", 150: "^", 300: "D"}

    # Create a single PDF file for all plots
    pdf_filename = "plots_0.8.13.17.21.pdf"
    with PdfPages(pdf_filename) as pdf:
        for axle_type in axle_types:
            for shoulder in shoulders:
                for p in p_values_dict[axle_type]:
                    # Create a new figure with a 2x2 grid of subplots
                    fig, axs = plt.subplots(2, 3, figsize=(15, 8))

                    # Remove the last subplot in the second row
                    fig.delaxes(axs[1, 2])

                    fig.suptitle(
                        f"Charts for max. tensile stress at the bottom of slab for BUC\ndue to {axle_type} Axle of {p} kN, {shoulder}"
                    )

                    for i, delta_t in enumerate(delta_t_values):
                        # Get the current subplot
                        ax = axs[i // 3, i % 3]

                        # Plot each value of k on the same subplot
                        for k in k_values:
                            S_values = []

                            for h in h_values:
                                # Calculate l(m) using the formula
                                l = ((E * h**3) / (12 * k * (1 - mu**2))) ** 0.25

                                # Calculate S(kN) using the function
                                S = calculate_S(
                                    axle_type, shoulder, k, p, h, l, delta_t
                                )
                                S_values.append(S)

                            # Plot S values for the current k with markers
                            ax.plot(
                                h_values,
                                S_values,
                                marker=markers[k],
                                label=f"k={k} MPa/m",
                                linestyle="-",
                                markersize=4,
                            )

                        # Set subplot properties
                        ax.set_title(f"ΔT={delta_t}°C")
                        ax.set_xlabel("h (m)")
                        ax.set_ylabel("S (kN)")
                        ax.grid(which="both", linestyle="-", linewidth=0.5)
                        ax.minorticks_on()
                        ax.legend()

                    # Adjust layout for better spacing
                    fig.tight_layout(rect=[0, 0, 1, 0.96])

                    # Save the 2x3 subplot figure to the PDF file
                    pdf.savefig()
                    plt.close()

                    print(
                        f"Plots for {axle_type}, {shoulder}, {p} kN added to {pdf_filename}"
                    )

    print(f"All plots saved to {pdf_filename}")


# Call the generatePlots function
generatePlots()
