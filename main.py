from tksheet import Sheet
from compute import main_compute
import ast
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as fd


def numerical_entry_callback(p):
    if str.isdigit(p) or p == "":
        return True
    else:
        return False


def ctrlEvent(event):
    if 12 == event.state and event.keysym == 'c':
        return
    else:
        return "break"


class MainGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.compute_options = {0: 'Standard', 1: 'Random', 2: 'Best of 1Mil'}
        self.compute_mode = 0
        self.team_size = 1
        self.player_data = {}

        self.geometry("1280x720")
        self.title('Elo Team Balancer')
        self.configure(background='dark blue')

        # Margin grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Centre grid config
        self.grid_columnconfigure(1, weight=16)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=16)
        self.grid_rowconfigure(1, weight=16)

        # Config for left frame containing input data
        self.table_frame = tk.Frame(self, bg='blue')
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(1, weight=9)

        # Config for centre button panel
        self.button_frame = tk.Frame(self, bg='yellow')
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(1, weight=1)

        # Config for right frame containing result data
        self.output_frame = tk.Frame(self)
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=9)

        # Placement of main three frames
        self.table_frame.grid(row=1, column=1, sticky="nswe")
        self.button_frame.grid(row=1, column=2, sticky="nswe")
        self.output_frame.grid(row=1, column=3, sticky="nswe")

        # Input table title
        self.input_sheet_title = ttk.Label(self.table_frame, text="Input Table of Players")
        self.input_sheet_title.grid(row=0, column=0)

        self.input_sheet_frame = tk.Frame(self.table_frame)
        self.input_sheet_frame.grid(row=1, column=0, sticky="nswe")
        self.input_sheet_frame.grid_columnconfigure(0, weight=1)
        self.input_sheet_frame.grid_rowconfigure(0, weight=1)

        # Input table
        self.input_sheet = Sheet(self.input_sheet_frame,
                                 empty_horizontal=0,
                                 empty_vertical=0,
                                 total_columns=3,
                                 paste_insert_column_limit=3,
                                 align="center",
                                 header_align="c",
                                 headers=["IGN", "Avg. Elo", "Elos"],
                                 data=[["" for _ in range(3)] for _ in range(12)],
                                 height=self.table_frame.winfo_height(),
                                 width=self.table_frame.winfo_width(),
                                 theme="dark",
                                 enable_edit_cell_auto_resize=True)
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
        self.input_sheet.grid(row=0, column=0, sticky="nswe")

        # Middle Button Strip
        # Input Control Frame
        self.input_control_frame = tk.LabelFrame(self.button_frame, text="Input Table Controls")
        self.input_control_frame.grid(row=0, column=0, sticky="we")
        self.input_control_frame.configure(background="red")
        self.input_control_frame.grid_columnconfigure(0, weight=1)
        self.input_control_frame.grid_rowconfigure(0, weight=1)
        self.input_control_frame.grid_rowconfigure(1, weight=1)

        # Row Count, Increment and Decrement Frame
        self.adjust_row_amount_frame = tk.Frame(self.input_control_frame)
        self.adjust_row_amount_frame.grid(row=0, column=0)

        # Row Count Label
        self.adjust_row_amount_label = ttk.Label(self.adjust_row_amount_frame, text="Number of Players: ")
        self.adjust_row_amount_label.grid(row=0, column=0)

        # Row Count Display
        self.vcmd = (self.register(numerical_entry_callback))
        self.adjust_row_amount_textbox_input_display = tk.Entry(self.adjust_row_amount_frame, validate='all',
                                                                validatecommand=(self.vcmd, '%P'), width=4)
        self.adjust_row_amount_textbox_input_display.bind('<Return>', self.setTableLength)
        self.adjust_row_amount_textbox_input_display.insert(tk.END, '12')
        self.adjust_row_amount_textbox_input_display.grid(row=0, column=1)

        # Increase Table Row Count
        self.adjust_row_amount_increment_button = ttk.Button(self.adjust_row_amount_frame,
                                                             text="+",
                                                             command=self.incrementEntry,
                                                             width=2)
        self.adjust_row_amount_increment_button.grid(row=0, column=2)

        # Decrease Table Row Count
        self.adjust_row_amount_decrement_button = ttk.Button(self.adjust_row_amount_frame,
                                                             text="-",
                                                             command=self.decrementEntry,
                                                             width=2)
        self.adjust_row_amount_decrement_button.grid(row=0, column=3)

        # Frame for Load and Save and Reset Button
        self.load_and_save_frame = tk.Frame(self.input_control_frame)
        self.load_and_save_frame.grid(row=1, column=0)

        # Load Button
        self.load_player_input_table_button = ttk.Button(self.load_and_save_frame,
                                                         text="Load",
                                                         command=self.load_input_table)
        self.load_player_input_table_button.grid(row=0, column=0)

        # Save Button
        self.save_player_input_table_button = ttk.Button(self.load_and_save_frame,
                                                         text="Save",
                                                         command=self.save_input_table)
        self.save_player_input_table_button.grid(row=0, column=1)

        # Reset Button
        self.reset_input_button = ttk.Button(self.load_and_save_frame,
                                             text="Reset",
                                             command=self.resetInputTable)
        self.reset_input_button.grid(row=0, column=2)

        # Compute Control Label Frame
        self.compute_control_frame = tk.LabelFrame(self.button_frame, text="Compute Controls")
        self.compute_control_frame.grid(row=1, column=0, sticky="we")
        self.compute_control_frame.configure(background="purple")
        self.compute_control_frame.grid_columnconfigure(0, weight=1)
        self.compute_control_frame.grid_rowconfigure(0, weight=1)
        self.compute_control_frame.grid_rowconfigure(1, weight=1)
        self.compute_control_frame.grid_rowconfigure(2, weight=1)

        # Compute Control Selection and Compute Button Frame
        self.compute_selection_frame = tk.Frame(self.compute_control_frame)
        self.compute_selection_frame.grid(row=0, column=0)
        self.compute_selection_frame.configure(background="green")

        # Compute Selection Control Label
        self.compute_selection_label = tk.Label(self.compute_selection_frame, text="Type:")
        self.compute_selection_label.grid(row=0, column=0)

        # Compute Selection Control
        self.compute_selection = ttk.Combobox(self.compute_selection_frame,
                                              justify="center",
                                              state="readonly",
                                              values=[*self.compute_options.values()],
                                              width=12)
        self.compute_selection.current(0)
        self.compute_selection.grid(row=0, column=1)

        # Compute Button
        self.compute_button = tk.Button(self.compute_selection_frame,
                                        text="Compute",
                                        command=self.compute)

        self.compute_button.grid(row=0, column=2)

        # Compute Control Selection and Compute Button Frame
        self.spinbox_frame = tk.Frame(self.compute_control_frame)
        self.spinbox_frame.grid(row=1, column=0)
        self.spinbox_frame.configure(background="red")

        # Team Size Label
        self.team_size_label = tk.Label(self.spinbox_frame, text="Team Size: ")
        self.team_size_label.grid(row=0, column=0)

        # Team Size Spinbox
        self.team_size_spinbox = ttk.Spinbox(self.spinbox_frame, from_=0, to=1000, width=4, state='readonly')
        self.team_size_spinbox.delete(0, "end")
        self.team_size_spinbox.insert(0, '1')
        self.team_size_spinbox.grid(row=0, column=1)

        # Compute Control Selection and Compute Button Frame
        self.compute_bar_frame = tk.Frame(self.compute_control_frame)
        self.compute_bar_frame.grid(row=2, column=0)
        self.compute_bar_frame.configure(background="blue")

        # Compute Progress Bar
        self.compute_progress_bar = ttk.Progressbar(self.compute_bar_frame,
                                                    orient='horizontal',
                                                    mode='determinate',
                                                    length=200)
        self.compute_progress_bar.grid(row=0, column=0)

        # Output Label
        self.output_text_title = ttk.Label(self.output_frame, text="Output Result")
        self.output_text_title.grid(row=0, column=0)

        # Output Text Box
        self.output_text = tk.Text(self.output_frame, width=1)
        self.output_text.configure(state="disabled")
        self.output_text.grid(row=1, column=0, sticky="nswe")
        self.output_text.bind("<Key>", lambda e: ctrlEvent(e))

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

    def save_input_table(self):
        file = fd.asksaveasfile(defaultextension='.txt', filetypes=[("Text file", ".txt"), ("All files", "*.*")])
        data = [x for x in self.input_sheet.get_sheet_data(return_copy=True, get_header=False, get_index=False) if
                x != ['', '', '']]
        file.write(str(data))
        file.close()

    def load_input_table(self):
        filename = fd.askopenfilename(filetypes=(("Text file", ".txt"), ("All files", "*.*")))
        if filename:
            with open(filename) as file:
                data = ast.literal_eval(file.read())
                self.input_sheet.set_sheet_data(data=data, redraw=True, verify=True)
                self.adjust_row_amount_textbox_input_display.delete(0, tk.END)
                self.adjust_row_amount_textbox_input_display.insert(tk.END, str(len(data)))

    def compute(self):
        self.compute_mode = self.compute_selection.current()
        raw = [x for x in self.input_sheet.get_sheet_data(return_copy=True, get_header=False, get_index=False) if
               x != ['', '', '']]
        self.player_data = {x[0]: int(x[1]) for x in raw}
        self.team_size = int(self.team_size_spinbox.get())
        message = main_compute(self.compute_mode, self.player_data, self.team_size)
        self.output_text.configure(state="normal")
        self.output_text.delete('1.0', 'end')
        self.output_text.insert('end', message)
        self.output_text.configure(state="disabled")


app = MainGUI()
app.mainloop()
