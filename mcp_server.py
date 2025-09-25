from mcp.server.fastmcp import FastMCP

mcp = FastMCP("info", host="0.0.0.0", port=8000)

@mcp.tool()
def get_info(name):
    """
    Get info of name includes: age, birtday
    """

    if "hang" in name:
        data = {
            "age": 18,
            "birtday": "25/10"
        }
    else:
        data = "Không có dữ liệu được lưu trữ"

    return data

@mcp.tool()
def get_people_family(name):
    """
    Get name of all people in family follow name
    """

    if "hang" in name:
        data = {
            "father": "Dam VT",
            "mother": "La TT",
            "sister": "Dam HG"
        }
    else:
        data = "Không có dữ liệu được lưu trữ"

    return data

if __name__ == "__main__":
    mcp.run(transport="sse")