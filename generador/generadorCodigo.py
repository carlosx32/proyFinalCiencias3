"""
An example how to generate angularjs code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""
from os import mkdir
from os.path import exists, dirname, join
import jinja2
from generadorDOT import get_entity_mm


def main(debug=False):

    this_folder = dirname(__file__)

    entity_mm = get_entity_mm(debug)

    # Build Person model from person.ent file
    modeloRestaurante = entity_mm.model_from_file(join(this_folder, 'restaurante.ent'))

    def is_entity(n):
        """
        Test to prove if some type is an entity
        """
        if n.type in modeloRestaurante.entities:
            return True
        else:
            return False

    def pythonType(s):
        """
        Maps type names from PrimitiveType to python.
        """
        return {
                'entero': 'int',
                'cadena': 'String',
                'boleano':'booleano',
                'dinero':'float',
                'caracter': 'char'
        }.get(s.name, s.name)

    def htmlType(s):
        """
        Maps type names from PrimitiveType to python.
        """
        return {
                'entero': 'number',
                'cadena': 'String',
                'boleano':'booleano',
                'dinero':'float',
                'caracter': 'char'
        }.get(s.name, s.name)

# Create output folder
    pagina_folder=join(this_folder,'../paginas')
    if not exists(pagina_folder):
        mkdir(pagina_folder)

    srcgen_folder = join(this_folder, '../paginas/')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register filter for mapping Entity type names to Python type names.
    jinja_env.tests['entity'] = is_entity
    jinja_env.filters['pythonType'] = pythonType
    jinja_env.filters['htmlType'] = htmlType

    # Load template
    template = jinja_env.get_template('python.template')
    template2= jinja_env.get_template('html.template')

    for entity in modeloRestaurante.entities:
        # For each entity generate python file crea los archivos
        #Direccion.py
        #Persona.py
        #Telefono.py
        with open(join(srcgen_folder,"%s.py" % entity.name.capitalize()), 'w') as f:
            f.write(template.render(entity=entity))
        with open(join(srcgen_folder,"%s.html" % entity.name.capitalize()), 'w') as f:
            f.write(template2.render(entity=entity))



if __name__ == "__main__":
    main()
