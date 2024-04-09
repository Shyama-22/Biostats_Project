import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar
import pandas as pd
import customtkinter

class CSVLoaderApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")# Set window size
        self.title("Statistical Test Predictor")# Set window title
  # Initialize variables
        self.file_path = None# To store path of uploaded file
        self.variables_of_interest = None
        self.df = None
        self.welcome_displayed = False  # Flag to track whether welcome page has been displayed

        self.welcome_page()# Display welcome page

    def welcome_page(self):
        if not self.welcome_displayed:
            # Create widgets for the welcome page
            welcome_label = customtkinter.CTkLabel(self, text="Welcome to Statistical Test Predictor", font=("Arial", 25, "bold"))
            welcome_label.pack(pady=20)


            self.upload_button = customtkinter.CTkButton(self, text="Upload CSV File", command=self.upload_csv)
            self.upload_button.pack(pady=20)

            self.welcome_displayed = True

    def upload_csv(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            print("CSV file uploaded successfully.")

            self.df = pd.read_csv(self.file_path)
            self.upload_button.pack_forget()
    # Proceed to variable selection
            self.select_variables_of_interest()
    def upload_csv(self):

        self.upload_button.pack_forget()
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            print("CSV file uploaded successfully.")
            self.df = pd.read_csv(self.file_path)

            self.reupload_button = customtkinter.CTkButton(self, text="Reupload CSV File", command=self.reupload_csv)
            self.reupload_button.pack(pady=10)

            self.next_button = customtkinter.CTkButton(self, text="Next", command=self.select_variables_of_interest)
            self.next_button.pack(pady=10)
# Re-upload CSV file if needed
    def reupload_csv(self):
        self.reupload_button.pack_forget()
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            print("CSV file reuploaded successfully.")
            self.df = pd.read_csv(self.file_path)
 # Show reupload and next buttons again for further actions
            self.reupload_button = customtkinter.CTkButton(self, text="Reupload CSV File", command=self.reupload_csv)
            self.reupload_button.pack(pady=10)


 # Select variables of interest from the uploaded CSV
    def select_variables_of_interest(self):
           # Prepare UI for variable selection: hide previous buttons and show next options
        self.variables_of_interest = []
        if self.file_path:
            self.upload_button.pack_forget()
            self.reupload_button.pack_forget()
            self.next_button.pack_forget()
 # Back button to return to previous step
            self.back_button = customtkinter.CTkButton(self, text="Back", command=self.upload_csv)
            self.back_button.pack(pady=10)

            self.next_button = customtkinter.CTkButton(self, text="Next", command=self.show_data_page)
            self.next_button.pack(pady=10)

            self.label_var = customtkinter.CTkLabel(self, text="Select Variables of Interest:", font=("Arial", 12, "bold"))
            self.label_var.pack(pady=5)

            self.variable_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=40, font=("Arial", 15))
            for col in self.df.columns:
                self.variable_listbox.insert(tk.END, col)
            self.variable_listbox.pack(pady=5)
 # Display selected data on a new page
    def show_data_page(self):
        selected_indices = self.variable_listbox.curselection()
        self.variables_of_interest = [self.variable_listbox.get(idx) for idx in selected_indices]

        self.back_button.pack_forget()
        self.next_button.pack_forget()
        self.label_var.pack_forget()
        self.variable_listbox.pack_forget()
     # Setup UI for showing selected data
        self.show_data_button = customtkinter.CTkButton(self, text="Show Data", command=self.show_data)
        self.show_data_button.pack(pady=10)

        self.show_details_button = customtkinter.CTkButton(self, text="Show Details", command=self.show_details)
        self.show_details_button.pack(pady=10)

    def show_data(self):
        self.next_button.pack_forget()
        if self.df is not None:
            selected_df = self.df[self.variables_of_interest]

            # Create a popup window with scrollable text
            popup = tk.Toplevel(self)
            popup.title("Selected Data")

            data_text = Text(popup, fg="black", bg="white", font=("Arial", 15), wrap="none")
            scrollbar = Scrollbar(popup, command=data_text.yview)
            data_text.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            data_text.pack(expand=True, fill="both", padx=20, pady=20)

            # Display the first 100 rows if the dataframe has more than 100 rows
            if len(selected_df) > 100:
                selected_df = selected_df.head(100)

            data_text.insert(tk.END, selected_df.to_string(index=False))

            # self.back_button = customtkinter.CTkButton(self, text="Back", command=self.select_variables_of_interest)
            # self.back_button.pack(pady=10)

            self.next_button = customtkinter.CTkButton(self, text="Next", command=self.one_variable_of_interest)
            self.next_button.pack(pady=10)

            # # Add a restart button to reset the app
            # restart_button = customtkinter.CTkButton(popup, text="Reset", command=self.restart_app)
            # restart_button.pack(pady=10)

    def show_details(self):
        self.next_button.pack_forget()
        if self.df is not None:
            details_text = f"Number of columns: {len(self.df.columns)}\n" \
                           f"Number of rows: {len(self.df)}\n" \
                           f"Columns: {', '.join(self.df.columns)}"

            # Create a popup window with scrollable text
            popup = tk.Toplevel(self)
            popup.title("Dataset Details")

            details_text_widget = Text(popup, fg="black", bg="white", font=("Arial", 15), wrap="word")
            scrollbar = Scrollbar(popup, command=details_text_widget.yview)
            details_text_widget.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            details_text_widget.pack(expand=True, fill="both", padx=20, pady=20)

            details_text_widget.insert(tk.END, details_text)

            # self.back_button = customtkinter.CTkButton(self, text="Back", command=self.select_variables_of_interest)
            # self.back_button.pack(pady=10)

            self.next_button = customtkinter.CTkButton(self, text="Next", command=self.one_variable_of_interest)
            self.next_button.pack(pady=10)

            # # Add a restart button to reset the app
            # restart_button = customtkinter.CTkButton(popup, text="Reset", command=self.restart_app)
            # restart_button.pack(pady=10)

    def restart_app(self):
        self.destroy()
        CSVLoaderApp().mainloop()




    #################################################################################################################

    def one_variable_of_interest(self):
        self.show_data_button.pack_forget()
        self.show_details_button.pack_forget()
        self.next_button.pack_forget()
        self.back_button.pack_forget()

 # Prompt user to select one variable of interest
        self.label_one_variable_of_interest = customtkinter.CTkLabel(self, text="Only one variable of interest? (Select Yes or No):",
                                                   font=("Arial", 12, "bold"))
        self.label_one_variable_of_interest.pack(pady=5)
# Button for selecting Yes
        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_one_sample)
        self.yes_button.pack(pady=5)
# Button for selecting NO
        self.no_button = customtkinter.CTkButton(self, text="No", command=self.askTwoVariableInterest)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def ask_one_sample(self):
        self.label_one_variable_of_interest.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_sample = customtkinter.CTkLabel(self, text="Is the data one sample? (Select Yes or No):", font=("Arial", 12, "bold"))
        self.label_sample.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_normal_distribution)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_TwoSample)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_normal_distribution(self):
        # Hide previous widgets/buttons
        self.label_sample.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        # Prompt user to select if the distribution is normal
        self.label_distribution = customtkinter.CTkLabel(self, text="Is the distribution normal? (Select Yes or No):", font=("Arial", 12, "bold"))
        self.label_distribution.pack(pady=5)

        # Button for selecting Yes
        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_normal_info)
        self.yes_button.pack(pady=5)

        # Button for selecting No
        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_binomial)
        self.no_button.pack(pady=5)

        # Restart button
        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    # def inference_concerning(self):
    #     self.label_distribution.pack_forget()
    #     self.yes_button.pack_forget()
    #     self.no_button.pack_forget()
    #     self.inference_concerning = customtkinter.CTkLabel(self,text="Inference concerning? (Select Yes or No):", font=("Arial", 12, "bold"))
    #     self.label_normal_info.pack(pady=5)
    #
    #     self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_normal_info)
    #     self.yes_button.pack(pady=5)
    #
    #     self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_other_test)
    #     self.no_button.pack(pady=5)

    def ask_normal_info(self):
        self.label_distribution.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_normal_info = customtkinter.CTkLabel(self, text="Do you know about mean, variance, and median? (Select Yes or No):", font=("Arial", 12, "bold"))
        self.label_normal_info.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_z_test)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_chi_square_test)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_binomial(self):
        self.label_distribution.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_binomial = customtkinter.CTkLabel(self, text="Is the data binomial? (Select Yes or No):", font=("Arial", 12, "bold"))
        self.label_binomial.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_binomial_size)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_poisson_test)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_poisson_test(self):
        self.label_binomial.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_poisson = customtkinter.CTkLabel(self, text="Is the distribution poisson? (Select Yes or No):",
                                                     font=("Arial", 12, "bold"))
        self.label_poisson.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_one_sample_poisson_test)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_non_parametric_test)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_binomial_size(self):
        self.label_binomial.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_size = customtkinter.CTkLabel(self, text="Is the 'n' large for the binomial distribution? (Select Yes or No):", font=("Arial", 12, "bold"))
        self.label_size.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_normal_binomial_test)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_exact_binomial_test)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def suggest_normal_binomial_test(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a one-sample binomial test using the normal theory method is suggested.")
        self.restart_app()

    def suggest_exact_binomial_test(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a one-sample binomial test using the exact method is suggested.")
        self.restart_app()

    def suggest_poisson_test(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a different statistical test may be more appropriate.")
        self.restart_app()

    def suggest_non_normal_test(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a different statistical test may be more appropriate.")
        self.restart_app()

    def suggest_z_test(self):
        messagebox.showinfo("Suggested Test","Based on the provided information, a one-sample z-test  is suggested.")
        self.restart_app()

    def suggest_other_test(self):
        messagebox.showinfo("Suggested Test","Based on the provided information, a one-sample binomial test using the normal theory method is suggested.")
        self.restart_app()

    def suggest_chi_square_test(self):
        messagebox.showinfo("Suggested Test","Based on the provided information, one sample t-test  or one sample CHI-square test for variance is suggested.")
        self.restart_app()

    def suggest_one_sample_poisson_test(self):
        messagebox.showinfo("Suggested Test","Based on the provided information, one sample poisson test is suggested.")
        self.restart_app()

    def suggest_non_parametric_test(self):
        messagebox.showinfo("Suggested Test","Based on the provided information, use of another underlying distribution or non parametric methods are suggested.")
        self.restart_app()

    ##############################################################################################################################
    ###################################################      Part 5      #########################################################
    ##############################################################################################################################
    def ask_oneSample(self):
        self.label_Person_time_data.pack_forget()
        #self.label_TimeOfEvent.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_onesample = customtkinter.CTkLabel(self, text="Is one sample problem? (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_onesample.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_oneSampleTest)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_incidenceRate)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_incidenceRate(self):
        self.label_onesample.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_incidenceRate = customtkinter.CTkLabel(self,
                                                 text="Is Incidence rate remains constant over time? (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_incidenceRate.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_twoSampleProblem)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_ComparisionOfSurvival)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_ComparisionOfSurvival(self):
        self.label_incidenceRate.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_comparisionOfSurvival = customtkinter.CTkLabel(self,
                                                 text="Intrested in comparision of survival curves of two groups with limited control of covariance? (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_comparisionOfSurvival.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_logrank)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_intrestInEffectOfSurvivalFactor)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_intrestInEffectOfSurvivalFactor(self):
        self.label_comparisionOfSurvival.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_interestInEffectOfSurvivalFactor = customtkinter.CTkLabel(self, text="Intrested in effects of survival risk factors on survival?(Willing to assume several curve comes from a weibull distribution) (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_interestInEffectOfSurvivalFactor.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_parameterSurvival)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_coxProportionalModel)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_twoSampleProblem(self):
        self.label_incidenceRate.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_twoSampleProblem = customtkinter.CTkLabel(self, text="Is two sample problem? (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_twoSampleProblem.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_twoSampleTest)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_test_of_trend)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def suggest_test_of_trend(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a test of trend for incidence rate is suggested")
        self.restart_app()

    def suggest_logrank(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a log-rank test is suggested")
        self.restart_app()

    def suggest_parameterSurvival(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a parametr survival method based on weibull distribution is suggested")
        self.restart_app()
    def suggest_coxProportionalModel(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a Cox proportional hazards model is suggested")
        self.restart_app()

    def suggest_oneSampleTest(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a one sample test for incidence rate is suggested")
        self.restart_app()

    def suggest_twoSampleTest(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a two-sample test is suggested.")
        self.restart_app()

    ##############################################################################################################################
    #################################################     Part 5 temp     ########################################################
    ##############################################################################################################################
    def ask_oneSample1(self):
        self.label_TimeOfEvent.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_onesample1 = customtkinter.CTkLabel(self, text="Is one sample problem? (Select Yes or No):",
                                                      font=("Arial", 12, "bold"))
        self.label_onesample1.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_oneSampleTest1)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_incidenceRate1)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_incidenceRate1(self):
        self.label_onesample1.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_incidenceRate1 = customtkinter.CTkLabel(self,
                                                          text="Is Incidence rate remains constant over time? (Select Yes or No):",
                                                          font=("Arial", 12, "bold"))
        self.label_incidenceRate1.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_twoSampleProblem1)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_ComparisionOfSurvival1)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_ComparisionOfSurvival1(self):
        self.label_incidenceRate1.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_comparisionOfSurvival1 = customtkinter.CTkLabel(self,
                                                                  text="Intrested in comparision of survival curves of two groups with limited control of covariance? (Select Yes or No):",
                                                                  font=("Arial", 12, "bold"))
        self.label_comparisionOfSurvival1.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_logrank1)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_intrestInEffectOfSurvivalFactor1)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_intrestInEffectOfSurvivalFactor1(self):
        self.label_comparisionOfSurvival1.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_interestInEffectOfSurvivalFactor1 = customtkinter.CTkLabel(self,
                                                                             text="Intrested in effects of survival risk factors on survival?(Willing to assume several curve comes from a weibull distribution) (Select Yes or No):",
                                                                             font=("Arial", 12, "bold"))
        self.label_interestInEffectOfSurvivalFactor1.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_parameterSurvival1)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_coxProportionalModel1)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_twoSampleProblem1(self):
        self.label_incidenceRate1.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_twoSampleProblem1 = customtkinter.CTkLabel(self,
                                                             text="Is two sample problem? (Select Yes or No):",
                                                             font=("Arial", 12, "bold"))
        self.label_twoSampleProblem1.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_twoSampleTest1)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_test_of_trend1)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def suggest_test_of_trend1(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a test of trend for incidence rate is suggested")
        self.restart_app()

    def suggest_logrank1(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a log-rank test is suggested")
        self.restart_app()

    def suggest_parameterSurvival1(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a parametr survival method based on weibull distribution is suggested")
        self.restart_app()

    def suggest_coxProportionalModel1(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a Cox proportional hazards model is suggested")
        self.restart_app()

    def suggest_oneSampleTest1(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a one sample test for incidence rate is suggested")
        self.restart_app()

    def suggest_twoSampleTest1(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a two-sample test is suggested.")
        self.restart_app()

    ##############################################################################################################################
    ###################################################      Part 6      #########################################################
    ##############################################################################################################################

    def ask_contingencyTable1(self):
        self.label_expected_value.pack_forget()           ########### Debug
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_contingencyTable1 = customtkinter.CTkLabel(self, text="Is 2x2 Contingency Table? (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_contingencyTable1.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_MantelHaenszelTest)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_contingencyTable2)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_contingencyTable2(self):
        self.label_contingencyTable1.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_contingencyTable2 = customtkinter.CTkLabel(self, text="Is 2xk Contingency Table? (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_contingencyTable2.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.askTrendOverBinomialProportions)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_ChiSquareTestrxc)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def askTrendOverBinomialProportions(self):
        self.label_contingencyTable2.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_TrendOverBinomialProportions = customtkinter.CTkLabel(self,
                                                 text="Is interested in trend over k binomial proportions? (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_TrendOverBinomialProportions.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_MantelExtensionTest)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_ChiSquareTest)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def suggest_ChiSquareTest(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, 'CHI-square test for heterogeneity for 2xk tables' is suggested")
        self.restart_app()

    def suggest_MantelHaenszelTest(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a Mantel Haenszel Test is suggested")
        self.restart_app()

    def suggest_MantelExtensionTest(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a Mantel Extension Test is suggested")
        self.restart_app()

    def suggest_ChiSquareTest2xk(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a Chi-Square Test for 2xk tables is suggested")
        self.restart_app()

    def suggest_ChiSquareTestrxc(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a Chi-Square Test for RxC tables is suggested")
        self.restart_app()

    ##############################################################################################################################
    ###################################################      Part 2      #########################################################
    ##############################################################################################################################

    def askCentralLimitTheorem(self):
        self.label_TwoSample.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_CentralLimitTheorem = customtkinter.CTkLabel(self,
                                                 text="Can central limit theorem be assumend to hold? (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_CentralLimitTheorem.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_oneWayANOVA)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.askCategorical)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def askCategorical(self):
        self.label_CentralLimitTheorem.pack_forget()      ########### Debug
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_Categorical = customtkinter.CTkLabel(self, text="Is data categorical? (Select Yes or No):",
                                                 font=("Arial", 12, "bold"))
        self.label_Categorical.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_rxcContingencyTable)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_KruskalWallisTest)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def suggest_oneWayANOVA(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a One-Way ANOVA Test is suggested")
        self.restart_app()

    def suggest_rxcContingencyTable(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a RxC Contingency Table method is suggested")
        self.restart_app()

    def suggest_KruskalWallisTest(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a Kruskal-Wallis test is suggested")
        self.restart_app()

    def next_page(self):
        self.label_sample.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()

        # Proceed to the next page or action




    ##############################################################################################################################
    ###################################################      Part 3      #########################################################
    ##############################################################################################################################

    def ask_sample_independent(self):
        self.label_Inference.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_sample_independent = customtkinter.CTkLabel(self,
                                                 text="Are samples independent? (Select yes or no):",
                                                 font=("Arial", 12, "bold"))
        self.label_sample_independent.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_Variance_different)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_paired_t_test)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def ask_Variance_different(self):
        self.label_sample_independent.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_Variance_different = customtkinter.CTkLabel(self,
                                                 text="Are variances of two samples significantly different? (Select yes or no):",
                                                 font=("Arial", 12, "bold"))
        self.label_Variance_different.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_two_sample_t_test_with_unequal_variance)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_two_sample_t_test_with_equal_variance)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def suggest_paired_t_test(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, Paired t-test is suggested")
        self.restart_app()


    def suggest_two_sample_t_test_with_unequal_variance(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, two sample t-test with unequal variance is suggested")
        self.restart_app()

    def suggest_two_sample_t_test_with_equal_variance(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, two sample t-test with equal variance is suggested")
        self.restart_app()

    ##############################################################################################################################
    ###################################################      Part 4      #########################################################
    ##############################################################################################################################

    # part 4
    def askTwoVariableInterest(self):
        self.label_one_variable_of_interest.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_TwoVariableInterest = customtkinter.CTkLabel(self,
                                                                text="Interested in relation between two variable? (Select Yes or No):",
                                                                font=("Arial", 12, "bold"))
        self.label_TwoVariableInterest.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.askContinuous)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.askContinuousOrBinary)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def askContinuous(self):
        self.label_TwoVariableInterest.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_Continuous = customtkinter.CTkLabel(self, text="Both variable are continuous? (Select Yes or No):",
                                                       font=("Arial", 12, "bold"))
        self.label_Continuous.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.askPredictionFromOneToAnother)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.askOneContinuousOneCategorical)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def askContinuousOrBinary(self):
        self.label_TwoVariableInterest.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_ContinuousOrBinary = customtkinter.CTkLabel(self,
                                                               text="Outcome variable continuous or variable? (Select Continuous or Binary):",
                                                               font=("Arial", 12, "bold"))
        self.label_ContinuousOrBinary.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Continuous", command=self.suggest_MultipleRegression)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="Binary", command=self.askTimeOfEvent)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def askTimeOfEvent(self):
        self.label_ContinuousOrBinary.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_TimeOfEvent = customtkinter.CTkLabel(self, text="Time of Event is important? (Select Yes or No):",
                                                        font=("Arial", 12, "bold"))
        self.label_TimeOfEvent.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_oneSample1)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_MultipleLogisticRegression)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def askOneContinuousOneCategorical(self):
        self.label_Continuous.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_OneContinuousOneCategorical = customtkinter.CTkLabel(self,
                                                                        text="One variable is continuous and other is categorical? (Select Yes or No):",
                                                                        font=("Arial", 12, "bold"))
        self.label_OneContinuousOneCategorical.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_ANOVA)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_RankCorrelation)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def askPredictionFromOneToAnother(self):
        self.label_Continuous.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_PredictionFromOneToAnothe = customtkinter.CTkLabel(self,
                                                                      text="Interested in predicting one variable from another? (Select Yes or No):",
                                                                      font=("Arial", 12, "bold"))
        self.label_PredictionFromOneToAnothe.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_SimpleRegression)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_pearsonOrRankCorrelation)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def suggest_RankCorrelation(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a Rank Correlation method is suggested")
        self.restart_app()

    def suggest_MultipleRegression(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, Multiple Regression is suggested")
        self.restart_app()

    def suggest_MultipleLogisticRegression(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, Multiple Logistic Regression is suggested")
        self.restart_app()

    def suggest_SimpleRegression(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, Simple Linear Regression is suggested")
        self.restart_app()

    def suggest_pearsonOrRankCorrelation(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, a Pearson Correlation is suggest if interested in studying correlation between two variables and both variables are normal and Rank Correlation method is suggested if variables are not normal")
        self.restart_app()


    def suggest_ANOVA(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, a ANOVA test is suggested")
        self.restart_app()

    ##############################################################################################################################
    ###################################################      Part 1      #########################################################
    ##############################################################################################################################


#part-1:
    def ask_TwoSample(self):
        self.label_sample.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_TwoSample = customtkinter.CTkLabel(self,
                                                 text="Two Sample problem? (Select yes or no):",
                                                 font=("Arial", 12, "bold"))
        self.label_TwoSample.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_Normal)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.askCentralLimitTheorem)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def ask_Normal(self):
        self.label_TwoSample.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_Normal = customtkinter.CTkLabel(self,
                                                 text="normally distributed and hold CLT? (Select yes or no):",
                                                 font=("Arial", 12, "bold"))
        self.label_Normal.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_Inference)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_4binomial)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def ask_Inference(self):
        self.label_Normal.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_Inference = customtkinter.CTkLabel(self,
                                                 text="Inference concerning? (Select yes or no):",
                                                 font=("Arial", 12, "bold"))
        self.label_Inference.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_sample_independent)          ####Jump to 3
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.ask_Inference_variance)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def ask_Inference_variance(self):
        self.label_Inference.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_Inference_variance = customtkinter.CTkLabel(self,
                                                 text="Inference concerning variance? (Select yes ):",
                                                 font=("Arial", 12, "bold"))
        self.label_Inference_variance.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.suggest_two_Sample_F_test)
        self.yes_button.pack(pady=5)

        # self.no_button = customtkinter.CTkButton(self, text="No", command=self.)
        # self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)
    def ask_4binomial(self):
        self.label_Normal.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_ask_binomial = customtkinter.CTkLabel(self,
                                                 text="Binomially distibuted? (Select yes or no):",
                                                 font=("Arial", 12, "bold"))
        self.label_ask_binomial.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_independent)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.Person_time_data)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)

    def ask_independent(self):
        self.label_ask_binomial.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_independent = customtkinter.CTkLabel(self,
                                                 text="Binomially distribution sample is independent? (Select yes or no):",
                                                 font=("Arial", 12, "bold"))
        self.label_independent.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.All_expected_values)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_McNemar)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def All_expected_values(self):
        self.label_independent.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_expected_value = customtkinter.CTkLabel(self,
                                                 text="Are all expected values >=5? (Select yes or no):",
                                                 font=("Arial", 12, "bold"))
        self.label_expected_value.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_contingencyTable1)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_Fisher)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def Person_time_data(self):
        self.label_ask_binomial.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.restart_button.pack_forget()

        self.label_Person_time_data = customtkinter.CTkLabel(self,
                                                 text="is this person time data? (Select yes or no):",
                                                 font=("Arial", 12, "bold"))
        self.label_Person_time_data.pack(pady=5)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.ask_oneSample)
        self.yes_button.pack(pady=5)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.suggest_non_parametric)
        self.no_button.pack(pady=5)

        self.restart_button = customtkinter.CTkButton(self, text="Reset", command=self.restart_app)
        self.restart_button.pack(pady=10)


    def suggest_two_Sample_F_test(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, Two Sample F-test is suggested")
        self.restart_app()


    def suggest_McNemar(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, McNemar's Exact Test is suggested")
        self.restart_app()

    def suggest_Fisher(self):
        messagebox.showinfo("Suggested Test",
                            "Based on the provided information, Fisher's exact Test is suggested")
        self.restart_app()

    def suggest_non_parametric(self):
        messagebox.showinfo("Suggested Test", "Based on the provided information, using of another underlying distribution or use of non-parametric methods are suggested")
        self.restart_app()


#main function
if __name__ == "__main__":
    app = CSVLoaderApp()
    app.mainloop()
