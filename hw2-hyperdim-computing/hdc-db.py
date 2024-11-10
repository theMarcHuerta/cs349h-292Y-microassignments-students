from hdc import *
import csv


class HDDatabase:

    def __init__(self):
        self.db = HDItemMem("db")
        self.string_codebook = HDCodebook("string_codebook")
        self.field_codebook = HDCodebook("field_codebook")

    def encode_string(self, value):
        if not self.string_codebook.has(value):
            self.string_codebook.add(value)
        return self.string_codebook.get(value)

    def decode_string(self, hypervec):
        distances = self.string_codebook.distance(hypervec)
        return min(distances, key=distances.get)

    def encode_row(self, fields):
        encoded_fields = []
        for field, value in fields.items():
            field_hv = self.encode_string(field)
            value_hv = self.encode_string(value)
            # Bind fieldwith val
            bound_hv = HDC.bind(field_hv, value_hv)
            encoded_fields.append(bound_hv)
        # Bundle all bound field-value pairs into a single row hypervector
        return HDC.bundle(encoded_fields)

    def decode_row(self, row_hv):
        decoded_fields = {}
        for field in self.field_codebook.all_keys():
            field_hv = self.encode_string(field)
            # Unbind the field from the row (a*b) + (c*d) if we unbind a
            # we should get (b) + (c*d)
            potential_value_hv = HDC.bind(row_hv, field_hv)
            # Find the closest matching value string in the string codebook
            # if we wta then we should get the closest thing to b
            closest_value = self.string_codebook.wta(potential_value_hv)
            decoded_fields[field] = closest_value
        return decoded_fields

    def add_row(self, primary_key, fields):
        row_hv = self.encode_row(fields)
        self.db.add(primary_key, row_hv)
        # if a field we aint seen yet, add it in
        for field in fields.keys():
            if not self.field_codebook.has(field):
                self.field_codebook.add(field)

    def get_row(self, key):
        row_hv = self.db.get(key)
        return self.decode_row(row_hv)

    def get_value(self, key, field):
        row_hv = self.db.get(key)
        decoded_row = self.decode_row(row_hv)
        return decoded_row.get(field, None) 

    def get_matches(self, field_value_dict, threshold=0.4):
        query_hv = self.encode_row(field_value_dict) #gonna use this to unbind
        distances = self.db.distance(query_hv)
        matches = {}
        for key, dist in distances.items():
            if dist <= threshold:
                matches[key] = dist  
        return matches

    def get_analogy(self, target_key, other_key, target_value):
        decoded_target_row = self.get_row(target_key)
        target_field = None
        for field, value in decoded_target_row.items():
            if value == target_value:
                target_field = field
                break
        other_value = self.get_value(other_key, target_field)
        return other_value, 0.0 


def load_json():
    data = {}
    with open("digimon.csv", "r") as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['Digimon']
            data[key] = rows
    return data


def build_database(data):
    HDC.SIZE = 10000
    db = HDDatabase()

    # gets the database and every row is passsed to add row
    for key, fields in data.items():
        db.add_row(key, fields)

    return db


def summarize_result(data, result, summary_fn):
    print("---- # matches = %d ----" % len(list(result.keys())))
    for digi, distance in result.items():
        print("%f] %s: %s" % (distance, digi, summary_fn(data[digi])))


def digimon_basic_queries(data, db):

    print("===== virus-plant query =====")
    thr = 0.4
    digis = db.get_matches({"Type": "Virus", "Attribute": "Plant"}, threshold=thr)
    summarize_result(data, digis, lambda row: "true match" if row["Type"] == "Virus" and row["Attribute"] == "Plant" else "false positive")

    print("===== champion query =====")
    thr = 0.4
    digis = db.get_matches({"Stage": "Champion"}, threshold=thr)
    summarize_result(data, digis, lambda row: "true match" if row["Stage"] == "Champion" else "false positive")


def digimon_test_encoding(data, db):
    strn = "tester"
    hv_test = db.encode_string(strn)
    rec_strn = db.decode_string(hv_test)
    print("original=%s" % strn)
    print("recovered=%s" % rec_strn)
    print("---")

    row = data["Wormmon"]
    hvect = db.encode_row(row)
    rec_row = db.decode_row(hvect)
    print("original=%s" % str(row))
    print("recovered=%s" % str(rec_row))
    print("---")


def digimon_value_queries(data, db):
    value = db.get_value("Lotosmon", "Stage")
    print("Lotosmon.Stage = %s" % value)

    targ_row = db.get_row("Lotosmon")
    print("Lotosmon" + str(targ_row))


def analogy_query(data, db):
    # Lotosmon is to Data as Imperialdramon PM is to <what field>

    targ_row = db.get_row("Lotosmon")
    other_row = db.get_row("Imperialdramon PM")
    print("Lotosmon has a a field with a Data value, what is the equivalent value in Imperialdramon PM's entry")
    value, dist = db.get_analogy(target_key="Lotosmon", other_key="Imperialdramon PM", target_value="Data")
    print("Lotosmon" + str(targ_row))
    print("Imperialdramon PM" + str(other_row))
    print("------")
    print("value: %s (dist=%f)" % (value, dist))
    print("expected result: Vaccine, the type of Imperialdramon PM")
    print("")


if __name__ == '__main__':
    data = load_json()
    db = build_database(data)
    digimon_test_encoding(data, db)
    digimon_basic_queries(data, db)
    digimon_value_queries(data, db)
    # digimon_test_encoding(data, db)
    analogy_query(data, db)
