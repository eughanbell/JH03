import PDBeEntry

def test_resolution_extraction(test_entry):
    test_entry["resolution"] = "1.34 A" # Valid float
    assert test_entry.extract_resolution() == 1.34
    test_entry["resolution"] = "7 A" # Valid int
    assert test_entry.extract_resolution() == 7
    test_entry["resolution"] = "1.34a A" # Invalid
    assert test_entry.extract_resolution() == None
    test_entry["resolution"] = "1.34" # Invalid
    assert test_entry.extract_resolution() == None
    test_entry["resolution"] = "1.34a A" # Invalid
    assert test_entry.extract_resolution() == None
    test_entry["resolution"] = "" # Invalid
    assert test_entry.extract_resolution() == None

def test_method_extraction(test_entry):
    test_entry["method"] = "X-ray" # Valid method
    assert test_entry.extract_method() == "X-ray"
    # Need to assert other valid methods pass

    test_entry["method"] = "X-rrray" # Invalid method
    assert test_entry.extract_method() == None
    test_entry["method"] = "" # Invalid
    assert test_entry.extract_method() == None

def test_chain_length_extraction(test_entry):
    test_entry["chains"] = "B/D=1-145" # Valid chain of length 145
    assert test_entry.extract_chain_length() == 145
    test_entry["chains"] = "B/D=73-100" # Valid chain of length 28
    assert test_entry.extract_chain_length() == 28
    test_entry["chains"] = "" # Invalid
    assert test_entry.extract_chain_length() == None
    test_entry["chains"] = "B/D73-100" # Invalid
    assert test_entry.extract_chain_length() == None
    test_entry["chains"] = "B/D=73100" # Invalid
    assert test_entry.extract_chain_length() == None
    test_entry["chains"] = "C/E=73-100" # Invalid
    assert test_entry.extract_chain_length() == None

test_entry = PDBeEntry({'id': '6II1', 'method': 'X-ray', 'resolution': '1.34 A', 'chains': 'B/D=1-145'})

test_resolution_extraction(test_entry)
test_method_extraction(test_entry)
test_chain_length_extraction(test_entry)