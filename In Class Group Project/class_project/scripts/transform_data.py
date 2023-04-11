import csv


def run():
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        with open('transformed_data.csv', 'w', newline='') as writecsvfile:
            fieldnames = ['state', 'type', 'date', 'source_key', 'amount']
            writer = csv.DictWriter(writecsvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                for year in range (2001, 2023):
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"1/1/{year}", 'amount': row[f'Jan {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"2/1/{year}", 'amount': row[f'Feb {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"3/1/{year}", 'amount': row[f'Mar {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"4/1/{year}", 'amount': row[f'Apr {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"5/1/{year}", 'amount': row[f'May {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"6/1/{year}", 'amount': row[f'Jun {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"7/1/{year}", 'amount': row[f'Jul {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"8/1/{year}", 'amount': row[f'Aug {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"9/1/{year}", 'amount': row[f'Sep {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"10/1/{year}", 'amount': row[f'Oct {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"11/1/{year}", 'amount': row[f'Nov {year}'] })
                    writer.writerow({'state': row['state'], 'type': row['type'], 'source_key':row['source key'], 'date': f"12/1/{year}", 'amount': row[f'Dec {year}'] })
                            

if __name__ == "__main__":
    run()