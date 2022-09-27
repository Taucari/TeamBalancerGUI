from tksheet import Sheet
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox


class MainGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1280x720")
        self.title('Elo Team Balancer')

        # Margin grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Centre grid config
        self.grid_columnconfigure(1, weight=16)
        self.grid_columnconfigure(2, weight=4)
        self.grid_columnconfigure(3, weight=16)
        self.grid_rowconfigure(1, weight=8)

        # Config for left frame containing input data
        self.table_frame = tk.Frame(self, bg='blue')
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(1, weight=9)

        # Config for centre button panel
        self.button_frame = tk.Frame(self, bg='yellow')
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        # Config for left frame containing result data
        self.output_frame = tk.Frame(self, bg='green')
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)

        # Placement of main three frames
        self.table_frame.grid(row=1, column=1, sticky="nswe")
        self.button_frame.grid(row=1, column=2, sticky="nswe")
        self.output_frame.grid(row=1, column=3, sticky="nswe")

        # Input table title
        self.input_sheet_title = ttk.Label(self.table_frame, text="Input Table of Players")
        self.input_sheet_title.grid(row=0, column=0)

        # Input table
        self.input_sheet = Sheet(self.table_frame,
                                 empty_horizontal=0,
                                 empty_vertical=0,
                                 total_columns=3,
                                 paste_insert_column_limit=3,
                                 align="w",
                                 header_align="c",
                                 headers=["IGN", "Avg. Elo", "Elos"],
                                 data=[["" for _ in range(3)] for _ in range(12)],
                                 height=self.table_frame.winfo_height(),
                                 width=self.table_frame.winfo_width())
        self.input_sheet.set_all_cell_sizes_to_text(redraw=True)
        self.input_sheet.total_columns(3)
        self.input_sheet.hide(canvas="top_left")
        self.input_sheet.enable_bindings()
        self.input_sheet.disable_bindings("row_height_resize",
                                          "rc_insert_column",
                                          "rc_delete_column",
                                          "rc_insert_row",
                                          "rc_delete_row")
        self.input_sheet.set_column_widths(column_widths=[120, 60, 240])
        self.input_sheet.grid(row=1, column=0, sticky="nswe")

        # Middle Button Strip
        self.input_control_frame = tk.LabelFrame(self.button_frame, text="Input Table Controls")
        self.input_control_frame.grid(row=0, column=0)

        self.adjust_row_amount_frame = tk.Frame(self.input_control_frame)
        self.adjust_row_amount_frame.grid(row=0, column=0)

        self.adjust_row_amount_label = ttk.Label(self.adjust_row_amount_frame, text="Number of Players: ")
        self.adjust_row_amount_label.grid(row=0, column=0)

        self.vcmd = (self.register(self.numerical_entry_callback))
        self.adjust_row_amount_textbox_input_display = tk.Entry(self.adjust_row_amount_frame, validate='all',
                                                                validatecommand=(self.vcmd, '%P'), width=4)
        self.adjust_row_amount_textbox_input_display.bind('<Return>', self.setTableLength)
        self.adjust_row_amount_textbox_input_display.insert(tk.END, '12')
        self.adjust_row_amount_textbox_input_display.grid(row=0, column=1)

        self.adjust_row_amount_increment_button = ttk.Button(self.adjust_row_amount_frame,
                                                             text="+",
                                                             command=self.incrementEntry,
                                                             width=2)
        self.adjust_row_amount_increment_button.grid(row=0, column=2)

        self.adjust_row_amount_decrement_button = ttk.Button(self.adjust_row_amount_frame,
                                                             text="-",
                                                             command=self.decrementEntry,
                                                             width=2)
        self.adjust_row_amount_decrement_button.grid(row=0, column=3)

        self.load_and_save_frame = tk.Frame(self.input_control_frame)
        self.load_and_save_frame.grid(row=1, column=0)

        self.load_player_input_table_button = ttk.Button(self.load_and_save_frame, text="Load")
        self.load_player_input_table_button.grid(row=0, column=0)

        self.save_player_input_table_button = ttk.Button(self.load_and_save_frame, text="Save")
        self.save_player_input_table_button.grid(row=0, column=1)

        self.reset_input_button = ttk.Button(self.input_control_frame,
                                             text="Reset Input Table",
                                             command=self.resetInputTable)
        self.reset_input_button.grid(row=2, column=0)

        # # Output table
        # self.output_sheet = Sheet(self.output_frame, show_x_scrollbar=False,
        #                           data=[[f"{r}, {c}" for c in range(3)] for r in range(12)])
        # self.output_sheet.enable_bindings()
        # self.output_sheet.grid(row=0, column=0, sticky="nswe")

    def numerical_entry_callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def incrementEntry(self):
        entry_data = int(self.adjust_row_amount_textbox_input_display.get())
        self.adjust_row_amount_textbox_input_display.delete(0, tk.END)
        self.adjust_row_amount_textbox_input_display.insert(tk.END, str(entry_data + 1))
        self.setTableLength()

    def decrementEntry(self):
        entry_data = int(self.adjust_row_amount_textbox_input_display.get())
        self.adjust_row_amount_textbox_input_display.delete(0, tk.END)
        self.adjust_row_amount_textbox_input_display.insert(tk.END, str(entry_data - 1))
        self.setTableLength()

    def setTableLength(self, event=None):
        if self.input_sheet.get_total_rows() == 1 and int(self.adjust_row_amount_textbox_input_display.get()) == 0:
            messagebox.showerror("Error", "The input table can not have less than 1 player.")
            self.incrementEntry()
        else:

            if int(self.adjust_row_amount_textbox_input_display.get()) > self.input_sheet.get_total_rows():
                self.input_sheet.insert_rows(
                    rows=int(self.adjust_row_amount_textbox_input_display.get()) - self.input_sheet.get_total_rows(),
                    redraw=True)
                self.input_sheet.recreate_all_selection_boxes()
                self.input_sheet.refresh(redraw_header=True, redraw_row_index=True)
            if int(self.adjust_row_amount_textbox_input_display.get()) < self.input_sheet.get_total_rows():
                for _ in range(
                        self.input_sheet.get_total_rows() - int(self.adjust_row_amount_textbox_input_display.get())):
                    self.input_sheet.delete_row(idx=self.input_sheet.get_total_rows() - 1, redraw=True)
                self.input_sheet.recreate_all_selection_boxes()
                self.input_sheet.refresh(redraw_header=True, redraw_row_index=True)

    def resetInputTable(self):
        row_heights, column_widths = self.input_sheet.get_row_heights(), self.input_sheet.get_column_widths()
        self.input_sheet.set_sheet_data(data=[["" for _ in range(len(column_widths))] for _ in range(len(row_heights))])
        self.input_sheet.set_column_widths(column_widths=[120, 60, 240])
        self.input_sheet.recreate_all_selection_boxes()
        self.input_sheet.refresh(redraw_header=True, redraw_row_index=True)


app = MainGUI()
app.mainloop()
