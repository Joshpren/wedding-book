from django.db.models.fields.files import FieldFile

def table(header, rows):
    table = "<table>\n"
    table += "  <tr>\n"
    for column in header:
        table += "    <th>{0}</th>\n".format(column.strip())
    table += "  </tr>\n"

    # Create the table's row data
    for row in rows:
        table += "  <tr>\n"
        for cell in row:
            if isinstance(cell, FieldFile):
                table += f"    <td><audio controls><source src=\"{ cell.url}\" type=\"audio/mpeg\"></audio></td>\n"
            else:
                table += "    <td>{0}</td>\n".format(cell)
        table += "  </tr>\n"

    table += "</table>"
    return table


def dropdown(options):
    dropdown = "<div class=\"dropdown\">"
    selectedOption = None
    dropdownOptions = "<div class=\"dropdown-options\">\n"
    for option in options:
        if option[0]:
            selectedOption = option[2]
            dropdownOptions += f"\t<div class=\"selected\" id={option[1]} onclick=\"selectMic({option[1]})\">{option[2]}</div>\n"
        else:
            dropdownOptions += f"\t<div id={option[1]} onclick=\"selectMic({option[1]})\">{option[2]}</div>\n"
    dropdownOptions += "</div>"
    dropdown += f"""<div class=\"dropdown-selected\" id=\"selected-mic\">
                    \t<i class=\"fa-solid fa-microphone \"></i>
                    \t<span>{selectedOption}</span>
                </div>"""
    dropdown += dropdownOptions
    dropdown += "</div>"
    return dropdown
        

def embedInForm(html, action):
    form = f"<form action=\"{action}\">\n"
    form += f"{html}\n"
    form += "<input type=\"submit\" value=\"Submit\">"
    return form + "</form>"