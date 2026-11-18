
import pandas as pd
from io import BytesIO

def export_to_excel(data, stock_symbol):
    if data is None or data.empty:
        return None

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(
            writer,
            sheet_name="Stock Analysis",
            index=True
        )

    output.seek(0)

    return output.getvalue()
