import quotation.api.helpers.base_name as names
import quotation.api.helpers.base_errors as errors
from quotation.api.helpers.service import Sql


class Provider:
    def select_user(self, args):
        query = """
        
                   
                """.format()
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, result[0]
