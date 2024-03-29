# %%
# !pip install pikepdf

import time

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import itertools
import string

import pikepdf
from tqdm import tqdm

import pikepdf

# my imports

window = tk.Tk()
# Start to describe the main window loop

# %%
# describe tkinter variables that we need
K = {'pdf_file_path' : tk.Variable(),
     'display_names' : tk.Variable()
     }

# %%


# %%


# describe window's parameters
window.resizable(0, 0)
window.title('UnlockPDF')
window.geometry('400x120')

window.columnconfigure(0, weight=2)
window.rowconfigure(0)

# a comand to close window in the end
def CloseWindow():
    window.quit()
    window.destroy()

# a comand to update window
def UpdateWindow():
    time.sleep(1)
    window.update_idletasks()

# window's structure
frame_upper = ttk.Frame(window, width=20, height=20)
frame_upper.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5)


frame_upper.columnconfigure(0, weight=4)

frame_upper.rowconfigure(0, weight=1)
frame_upper.rowconfigure(1, weight=1)
frame_upper.rowconfigure(2, weight=10)

# main function that do everything after you pick files
def convertPDF(event=None):
    file_paths = filedialog.askopenfilenames(
        initialdir='',
        title="Open your PDF files",
        filetypes=(("PDF files", "*.pdf"),))
    files_count = len(file_paths)
    # after files are picked, they are converted in a cycle
    for single_file_path in file_paths:
        # there we open files and update info line in the window
        try:
            # then we add suffix to file name
            K['pdf_file_path'].set(single_file_path)
            K['display_names'].set(K['display_names'].get() + '\n' + single_file_path)
            upload_pdf_line.configure(text=K['pdf_file_path'].get())
            pdf = pikepdf.open(single_file_path, allow_overwriting_input=True)
            filename = str(K['pdf_file_path'].get()).split('/')[-1]
            new_filename = filename[0:-4]+'_unlocked'+'.pdf'
            
            # reconstruct the path for a new file
            slash = '/'
            new_path = slash.join(str(K['pdf_file_path'].get()).split('/')[0:-1])+slash+new_filename
            pdf.save(new_path)
            
            # optional wait period
            # time.sleep(0.5)
            print(new_path, ' is ready')
            window.update()
            
        # except pikepdf._core.PasswordError:
        #     def guess_password():
        #         chars = string.ascii_lowercase + string.digits
        #         attempts = 0
        #         for password_length in range(1,6):
        #             for guess in itertools.product(chars, repeat=password_length):
        #                 attempts += 1
        #                 guess = ''.join(guess)
        #                 try:
        #                     K['pdf_file_path'].set(single_file_path)
        #                     K['display_names'].set(K['display_names'].get() + '\n' + single_file_path)
        #                     upload_pdf_line.configure(text=K['pdf_file_path'].get())
        #                     pdf = pikepdf.open(single_file_path, allow_overwriting_input=True)
        #                     filename = str(K['pdf_file_path'].get()).split('/')[-1]
        #                     new_filename = filename[0:-4]+'_unlocked'+'.pdf'
                            
        #                     # reconstruct the path for a new file
        #                     slash = '/'
        #                     new_path = slash.join(str(K['pdf_file_path'].get()).split('/')[0:-1])+slash+new_filename
        #                     pdf.save(new_path)
                            
        #                     # optional wait period
        #                     # time.sleep(0.5)
        #                     print(new_path, ' is ready')
        #                     window.update()
                            
        #                 except pikepdf._core.PasswordError:
        #                     if attempts % 1000 == 0:
        #                         print(guess, attempts)
        #                     pass
        #     guess_password()
        
        
        # based on https://thepythoncode.com/article/crack-pdf-file-password-in-python
        # you can replace wordlist.txt with your own base of common passwords
        # that file can be measured in gigabytes, but it'd would make it slow
        except:
            # load password list
            passwords = [ line.strip() for line in open("wordlist.txt") ]

            # iterate over passwords
            for password in tqdm(passwords, "Decrypting PDF"):
                try:
                    # open PDF file
                    with pikepdf.open(single_file_path, password=password) as pdf:
                        # Password decrypted successfully, break out of the loop
                        print("[+] Password found:", password)
                        filename = str(K['pdf_file_path'].get()).split('/')[-1]
                        new_filename = filename[0:-4]+'_unlocked'+'.pdf'
                        
                        # reconstruct the path for a new file
                        slash = '/'
                        new_path = slash.join(str(K['pdf_file_path'].get()).split('/')[0:-1])+slash+new_filename
                        pdf.save(new_path)
                        
                        # optional wait period
                        # time.sleep(0.5)
                        print(new_path, ' is ready')
                        window.update()                        
                        break
                except pikepdf._core.PasswordError as e:
                    # wrong password, just continue in the loop
                    continue
            
        
        files_count -= 1
        if files_count == 0:
            #kill window
            print('Task completed')
            CloseWindow()

# that's the header of the window
upload_csv_label = ttk.Label(frame_upper, text="Pick your PDF files to unlock", width=150, justify='center')
upload_csv_label.grid(column=0, row=0, sticky=tk.NSEW, padx=0, pady=5, columnspan=1)

# that's the button
upload_csv_button = tk.Button(frame_upper, text='Browse', command=convertPDF, width=20)
upload_csv_button.grid(column=0, row=1, padx=0, pady=5, sticky=tk.NSEW)

# and that's a line for a currently converted file
upload_pdf_line = ttk.Label(frame_upper, text=K['display_names'].get(), wraplength=300, borderwidth=1, relief='sunken', width=50, background='black', foreground='white')
upload_pdf_line.grid(column=0, row=2, padx=0, rowspan=10, pady=5, sticky=tk.NSEW)    

# %%
# here we initate this window
window.mainloop()

# %%
# letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# Letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
# numbers = ['1','2','3','4','5','6','7','8','9','0']

# set = letters + Letters + numbers
# set = numbers



# lenght = len(set)
# print(lenght)
# for i in range(lenght):
#     print(str(set[i]))
# for i in range(lenght):
#     for k in range(lenght):
#         print(str(set[i])+str(set[k]))
# for i in range(lenght):
#     for k in range(lenght):
#         for j in range(lenght):
#             print(str(set[i])+str(set[k])+str(set[j]))
# for i in range(lenght):
#     for k in range(lenght):
#         for j in range(lenght):
#             for l in range(lenght):
#                 print(str(set[i])+str(set[k])+str(set[j])+str(set[l]))

# %%
# import itertools

# def batched(iterable, n):
#     # batched('ABCDEFG', 3) → ABC DEF G
#     if n < 1:
#         raise ValueError('n must be at least one')
#     it = iter(iterable)
#     while batch := tuple(islice(it, n)):
#         yield batch
        
# print(batched(set, 2))

# %%
# def combinations(iterable, r):
#     # combinations('ABCD', 2) → AB AC AD BC BD CD
#     # combinations(range(4), 3) → 012 013 023 123
#     pool = tuple(iterable)
#     n = len(pool)
#     if r > n:
#         return
#     indices = list(range(r))
#     yield tuple(pool[i] for i in indices)
#     while True:
#         for i in reversed(range(r)):
#             if indices[i] != i + n - r:
#                 break
#         else:
#             return
#         indices[i] += 1
#         for j in range(i+1, r):
#             indices[j] = indices[j-1] + 1
#         yield tuple(pool[i] for i in indices)
# display(combinations(set, r=2))

# %%



                
                

            # uncomment to display attempts, though will be slower
            #print(guess, attempts)




