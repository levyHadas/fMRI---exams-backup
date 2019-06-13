import os
import datetime
import shutil


class Params:
    MAIN_PATH = "M:\\clinica\\patients\\Full_Scans"
    SUB_PATH = "Analysis\\func"
    TASKS_FOLDER_INIT = "Se"
    STR_IN_FILES_TO_REMOVE = "avol"
    STR_IN_FILES_TO_KEEP1 = "meanavol"
    STR_IN_FILES_TO_KEEP2 ="rp_avol"
    YEAR_TO_BACKUP = str (datetime.datetime.now().year - 1)
    EXTERNAL_DRIVE_MAIN_PATH = "F:\\FMRI"
    DTI_FOLDER_NAME = "\\DTI_patients"

class Errors:
	FOLDER_MISSING = "ERROR: Backup was not found for patient:"+" "
	FILES_NUM_NOT_EQUAL = "ERROR: The files number in patient folder is not equal at src and trg for patient:"+" "
	FOLDER_SIZE_NOT_EQUAL = "ERROR: The folder size is not equal at src and trg for patient:"+" "
	SUCCESS = "SUCCESS: back up test finished Successfully"




def month_number_to_name(month_num):

    month_dic = {'test':'month','1':'January' ,'2':'February','3':'March','4':'April','5':'May','6':'June','7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}

    return month_dic.get(month_num)




def create_src_month_path (month_num):

	month_folder_name = month_num + '_' + month_number_to_name(month_num)
	src_month_path = os.path.join(Params.MAIN_PATH, month_folder_name,"2016") #for the old backup

	return src_month_path





def create_backup_path (month_num):

	dst_new_folder = month_num + '_' + Params.YEAR_TO_BACKUP
	backedup_path = os.path.join(Params.EXTERNAL_DRIVE_MAIN_PATH, Params.YEAR_TO_BACKUP, dst_new_folder)

	return backedup_path





def get_patients_paths_and_names (src_month_path):
    patients_names = []
    patients_paths = []

    for patient_name in os.listdir (src_month_path):
        patients_names.append(patient_name)
        patients_paths.append(os.path.join (src_month_path, patient_name) )

    return patients_paths, patients_names
	








def delete_unnecessary_files(patients_paths):
	counter = 0

	for single_patient_path in patients_paths: #go through the list of all the patients folders in the
		if Params.DTI_FOLDER_NAME not in single_patient_path :
			for task_name in os.listdir( os.path.join(single_patient_path, Params.SUB_PATH) ): # go through the list of all tasks names for each patient
				counter +=1
				if Params.TASKS_FOLDER_INIT in task_name:

					task_path = os.path.join(single_patient_path, Params.SUB_PATH, task_name)
					print(task_path)
					for file_name in os.listdir(task_path): #go through the list of all files in task folder

						if (Params.STR_IN_FILES_TO_REMOVE in file_name) and (Params.STR_IN_FILES_TO_KEEP1 not in file_name) and (Params.STR_IN_FILES_TO_KEEP2 not in file_name): #we want to remove all files that contains STR_IN_FILES_TO_REMOVE (avol)
							#but keep the meanavol and the rp_avol fiels
							#os.remove(os.path.join(task_path , file_name)) # use after finished test
							os.rename(os.path.join(task_path,file_name) , os.path.join(task_path,file_name+str(counter)))
							shutil.move( os.path.join(task_path,file_name+str(counter))  , os.path.join("M:\\clinica\\patients\\Trash") ) #only for testing backup



def copy_to_external_drive(src_path, dst_path):

	shutil.copytree(src_path, dst_path)
	

def get_num_of_file(path):

	files_sum = 0;
	dirs_sum = 0;
	for _, dirs, files in os.walk(path):
		files_sum += len(files)
		dirs_sum += len(dirs)


def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            total_size += os.path.getsize( os.path.join(dirpath, f) )

    return total_size



def test_backup (src_names, trg_names, src_path, trg_path):
	
	errors = False
    
	for patient_name_src in src_names:
		folder_exist = False
		files_num_equal = False
		folder_size_equal = False
		
		for patient_name_trg in trg_names:
			if patient_name_src == patient_name_trg:
				
				folder_exist = True

				if get_num_of_file ( os.path.join(src_path,patient_name_src) ) == get_num_of_file( os.path.join(trg_path,patient_name_trg) ):
					files_num_equal = True

				if get_folder_size( os.path.join(src_path,patient_name_src) ) == get_folder_size( os.path.join (trg_path,patient_name_trg) ):
					folder_size_equal = True
					
				break
				
		if folder_exist == False:
			print (Errors.FOLDER_MISSING + patient_name_src)
			errors = True
		else:
			if files_num_equal == False:
				print (Errors.FILES_NUM_NOT_EQUAL + patient_name_src)
				errors = True
			if folder_size_equal == False:
				print (Errors.FOLDER_SIZE_NOT_EQUAL + patient_name_src)
				errors = True
	
	if errors == False:
		print (Errors.SUCCESS)





def main():

	month_num = raw_input("Please enter the number of the month you wish to backup")


	src_month_path = create_src_month_path (month_num)
	backedup_path = create_backup_path (month_num)
	
	
	patients_paths_src, patients_names_src = get_patients_paths_and_names(src_month_path)



	delete_unnecessary_files(patients_paths_src)
	copy_to_external_drive(src_month_path,backedup_path)

	patients_paths_trg, patients_names_trg = get_patients_paths_and_names(backedup_path)

	test_backup (patients_names_src, patients_names_trg, src_month_path, backedup_path)






main()


