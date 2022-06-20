# Code developed by Rahul Goel
# github :- rahulgoel11

import pandas as pd

def json_flatten(json_data,list_split_to_many=False,ignore_parent_key=None):
    '''
    To flatten the Json data in relational format
    :param json_data: Input data to be flattend, should be dict or list of dict
    :param list_split_to_many: If the final node list data should be splitted to one to many relation
    :param ignore_parent_key: Parent Keys to be ignored should be string or list
    :return: returns Dataframe of flattend json
    '''
    if type(json_data) == dict:
        json_data = [json_data]
    
    if type(json_data) == list and len(json_data) > 0:
        if type(json_data[0]) == dict:
            id_df = pd.DataFrame(json_data).reset_index().rename(columns={"index": "id_col"})
            if ignore_parent_key != None:
                if type(ignore_parent_key) != list:
                    ignore_parent_key = [ignore_parent_key]
                filtered_cols = list(set(id_df.columns.to_list()) - set(ignore_parent_key))
                id_df = id_df[filtered_cols]
            final_dict_df = id_df['id_col'].to_frame()
            for col_name in id_df.drop('id_col', axis=1).columns:
                final_master = id_df['id_col'].to_frame()
                child_cols = []

                check = True

                while check:

                    if any(col_name + '_' in srchstr for srchstr in final_master.columns):
                        master_flag = True
                        col_name_master = [col for col in final_master.columns if col_name + '_' in col]

                        col_name_master = list(set(col_name_master) - set(child_cols))
                        child_cols.extend(col_name_master)
                        temp_df_master = final_master[['id_col'] + col_name_master]
                        temp_df_master['temp_index'] = temp_df_master.reset_index().index
                    else:
                        master_flag = False
                        temp_df = id_df[['id_col', col_name]]

                    col_processed = 0
                    if master_flag:
                        col_names = [col for col in temp_df_master.columns if col not in ['temp_index', 'id_col']]
                    else:
                        col_names = [col for col in temp_df.columns if col not in ['temp_index', 'id_col']]

                    for cols in col_names:
                        if master_flag:
                            temp_df = temp_df_master[['id_col','temp_index',cols]]
                        if temp_df[cols].dropna().shape[0] > 0:
                            if type(temp_df[cols].dropna().reset_index(drop=True).iloc[0]) == list:
                                if max(temp_df[cols].str.len()) <= 1:
                                    temp_df[cols] = temp_df[cols].explode()
                                else:
                                    explode_temp = temp_df[cols].explode().to_frame()
                                    temp_df = temp_df.drop(cols, axis=1).join(explode_temp, how='left')

                            if temp_df[cols].dropna().shape[0] > 0:
                                if type(temp_df[cols].dropna().reset_index(drop=True).iloc[0]) == dict:
                                    if master_flag:
                                        drill_down_df = temp_df[~temp_df[cols].isna()].reset_index(drop=True).join(
                                            pd.DataFrame(temp_df.loc[~temp_df[cols].isna()][cols].to_list())).set_index(
                                            'temp_index')
                                        final_master = final_master.join(
                                            drill_down_df[list(set(drill_down_df.columns) - set(temp_df.columns))].add_prefix(
                                                cols + '_'),
                                            how='left', on='temp_index')
                                    else:
                                        drill_down_df = temp_df[~temp_df[cols].isna()].reset_index().drop(cols, axis=1).join(
                                            pd.DataFrame(temp_df.loc[~temp_df[cols].isna(), cols].to_list())).set_index('index')
                                        final_master = final_master.join(
                                            drill_down_df[list(set(drill_down_df.columns) - set(temp_df.drop(cols, axis=1).columns))].add_prefix(
                                                cols + '_'),
                                            how='left')
                                        final_master['temp_index'] = final_master.reset_index().index

                                    temp_df = temp_df.drop(cols, axis=1)
                                    if master_flag:
                                        final_master = final_master.drop(cols, axis=1)

                                    col_processed += 1
                                else:
                                    if master_flag is False and cols != 'id_col':
                                        final_master = final_master.join(temp_df.set_index('id_col'), how='left', on='id_col')
                            else:
                                    if master_flag is False and cols != 'id_col':
                                        final_master = final_master.join(temp_df.set_index('id_col'), how='left', on='id_col')
                        else:
                            if master_flag is False and cols != 'id_col':
                                final_master = final_master.join(temp_df.set_index('id_col'), how='left', on='id_col')

                    if col_processed == 0:
                        check = False

                if 'temp_index' in final_master.columns:
                    final_master = final_master.drop('temp_index', axis=1)
                final_dict_df = final_dict_df.join(final_master.set_index('id_col'), how='left', on='id_col')

            final_dict_df = final_dict_df.reset_index(drop=True).drop('id_col', axis=1)

            if list_split_to_many:
                for cols in final_dict_df.columns:
                    if type(final_dict_df[cols].dropna().iloc[0]) == list:
                        if max(final_dict_df[cols].str.len()) <= 1:
                            final_dict_df[cols] = final_dict_df[cols].explode()
                        else:
                            explode_temp = final_dict_df[cols].explode().to_frame()
                            final_dict_df = final_dict_df.drop(cols, axis=1).join(explode_temp, how='left')

            return final_dict_df.reset_index(drop=True)
        else:
            raise Exception("Data elements not in Dict")
    else:
        raise Exception("Data length is 0")