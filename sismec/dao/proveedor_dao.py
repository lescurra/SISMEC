from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import utils as utils_dao
from django.db import connection


def getProveedorFiltro(filtros):
    object_list = []
    query = '''SELECT row_number() over (ORDER BY p.id), p.id, p.nombres, p.ruc, p.direccion, p.telefono, p.mail
        FROM proveedor AS p'''
    query_var = []

    if filtros['search'] != '':
        query += '''
          WHERE UPPER(p.nombres) like UPPER(%s)'''
        query_var = ['%' + filtros['search'] + '%']
    query += '''
      ORDER BY p.id'''

    pagination = utils_dao.paginationData(query, query_var, filtros)

    total_row = pagination['total_row']
    row_per_page = pagination['row_per_page'] if 'row_per_page' in pagination else ROW_PER_PAGE
    page = pagination['page']

    if total_row > 0:
        cursor = connection.cursor()
        try:
            query_row_page = 'SELECT * FROM(' + query + ') AS pagination LIMIT %s OFFSET (%s - 1) * %s'
            query_var_page = query_var
            query_var_page.append(row_per_page)
            query_var_page.append(page)
            query_var_page.append(row_per_page)
            cursor.execute(query_row_page, query_var_page)

            for i in cursor.fetchall():
                data = {'row_number': i[0],
                        'id': i[1],
                        'nombres': i[2],
                        'ruc': i[3],
                        'direccion':i[4],
                        'telefono': i[5],
                        'mail': i[6],
                        }
                object_list.append(data)

        except Exception as e:
            print(e.args)
        finally:
            cursor.close()
    return object_list, pagination