from mcp.server.fastmcp import FastMCP

# Khởi tạo server
mcp = FastMCP("info")

@mcp.tool()
def get_info(name: str):
    """
    Get info of name includes: age, birthday
    """
    if "hang" in name.lower():
        return {
            "age": 18,
            "birthday": "25/10"
        }
    return "Không có dữ liệu được lưu trữ"

@mcp.tool()
def get_age(name: str):
    """
    Get age of person by name
    """
    if "hang" in name.lower():
        return 18
    return "Không có dữ liệu được lưu trữ"

@mcp.tool()
def get_people_family(name: str):
    """
    Get name of all people in family follow name
    """
    if "hang" in name.lower():
        return {
            "father": "Dam VT",
            "mother": "La TT",
            "sister": "Dam HG"
        }
    return "Không có dữ liệu được lưu trữ"

# if __name__ == "__main__":
#     # Chỉ cần run trực tiếp, FastMCP Cloud sẽ quản lý asyncio loop
#     mcp.run(transport="sse")
