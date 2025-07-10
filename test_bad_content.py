from content_parser import load_and_validate_content_yml, ContentValidationError

if __name__ == "__main__":
    try:
        load_and_validate_content_yml("bad_content.yml")
        print("NO ERROR: Validation passed (unexpected)")
    except ContentValidationError as e:
        print("VALIDATION ERROR:", e)
