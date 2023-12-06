def clean_link(link):
    # Define the part to be removed from the link
    part_to_remove = "xac-thuc-nguoi-dung.html?url=/"

    # Check if the link contains the part to remove
    if part_to_remove in link:
        # Remove the part and return the cleaned link
        return link.replace(part_to_remove, "")
    else:
        # If the part is not in the link, return the link unchanged
        return link

# Example usage
example_link = "https://alonhadat.com.vn/xac-thuc-nguoi-dung.html?url=/biet-thu-van-phu-vi-tri-cuc-dep-kinh-doanh-van-phong-o-to-tranh-via-he-rong-nh-13731534.html"
cleaned_link = clean_link(example_link)
print(cleaned_link)
