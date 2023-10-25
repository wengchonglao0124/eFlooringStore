from flask import Blueprint
from . import db
from .models import FlooringType, Specification, ProjectPhoto, Flooring, Order, OrderDetail
from datetime import datetime


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# function to put some seed data in the database
@admin_bp.route('/dbseed')
def dbseed():
    natural_type = FlooringType(id='ft01', type='Natural')
    hybrid_type = FlooringType(id='ft02', type='Hybrid')
    laminate_type = FlooringType(id='ft03', type='Laminate')
    vinyl_type = FlooringType(id='ft04', type='Vinyl')
    tile_type = FlooringType(id='ft05', type='Tile')

    try:
        db.session.add(natural_type)
        db.session.add(hybrid_type)
        db.session.add(laminate_type)
        db.session.add(vinyl_type)
        db.session.add(tile_type)
        db.session.commit()
    except:
        return 'There was an issue adding the flooringTypes in dbseed function'


    natural_timber_specification1 = Specification(id="sp11", size="14 × 120 × 600mm", component="UV coating, Timber veneer, Engineered Plywood Core", area_per_box=1.08, pieces_per_box=15)
    natural_timber_specification2 = Specification(id="sp12", size="14 × 190 x 1900mm", component="UV coating, Timber veneer, Engineered Plywood Core", area_per_box=2.17, pieces_per_box=6)
    natural_bamboo_specification = Specification(id="sp13", size="14 × 190 x 1830mm", component="UV coating, Bamboo veneer, Engineered Plywood Core", area_per_box=2.09, pieces_per_box=6)

    hybrid_timber_specification = Specification(id="sp21", size="8.5 × 190 x 1900mm", component="UV coating, Timber veneer, Engineered Rigid Core, Cork Backing", area_per_box=1.81, pieces_per_box=5)
    hybrid_bamboo_specification = Specification(id="sp22", size="8 × 142 × 1850mm", component="UV coating, Bamboo veneer, Engineered Rigid Core, Cork Backing", area_per_box=1.58, pieces_per_box=6)
    hybrid_SPC_specification = Specification(id="sp23", size="6 × 230 x 1500mm", component="UV coating, Durable layer, Engineered Rigid Core, Cork Backing", area_per_box=2.07, pieces_per_box=6)

    laminate_specification = Specification(id="sp31", size="8 × 167 × 1215mm", component="UV coating, Durable veneer, High-density fibre", area_per_box=1.61, pieces_per_box=8)

    vinyl_specification = Specification(id="sp41", size="1423 × 229 × 4.5mm", component="UV coating, Vinyl", area_per_box=2.61, pieces_per_box=8)

    tile_600_specification = Specification(id="sp51", size="600 × 600mm", component="Polished Finish", area_per_box=1.44, pieces_per_box=4)
    tile_800_specification = Specification(id="sp52", size="800 × 800mm", component="Polished Finish", area_per_box=2.56, pieces_per_box=4)

    try:
        db.session.add(natural_timber_specification1)
        db.session.add(natural_timber_specification2)
        db.session.add(natural_bamboo_specification)

        db.session.add(hybrid_timber_specification)
        db.session.add(hybrid_bamboo_specification)
        db.session.add(hybrid_SPC_specification)

        db.session.add(laminate_specification)

        db.session.add(vinyl_specification)

        db.session.add(tile_600_specification)
        db.session.add(tile_800_specification)
        db.session.commit()
    except:
        return 'There was an issue adding the specifications in dbseed function'


    natural_flooring1 = Flooring(id="f1101", type_id=natural_type.id, subtype="Herribone Timber", colour="Natural", specification_id=natural_timber_specification1.id, price=236.50, discount=1, image="f1101.png")
    natural_flooring2 = Flooring(id="f1201", type_id=natural_type.id, subtype="Timber", colour="American Walnut", specification_id=natural_timber_specification2.id, price=186.50, discount=0.9, image="f1201.png")
    natural_flooring3 = Flooring(id="f1202", type_id=natural_type.id, subtype="Timber", colour="Smoulder Oak", specification_id=natural_timber_specification2.id, price=186.50, discount=1, image="f1202.png")
    natural_flooring4 = Flooring(id="f1301", type_id=natural_type.id, subtype="Bamboo", colour="Honey", specification_id=natural_bamboo_specification.id, price=196.50, discount=1, image="f1301.png")
    natural_flooring5 = Flooring(id="f1302", type_id=natural_type.id, subtype="Bamboo", colour="White Wash", specification_id=natural_bamboo_specification.id, price=196.50, discount=0.95, image="f1302.png")

    hybrid_flooring1 = Flooring(id="f2101", type_id=hybrid_type.id, subtype="SPT Timber", colour="Grey Wash Oak", specification_id=hybrid_timber_specification.id, price=157.50, discount=1, image="f2101.png")
    hybrid_flooring2 = Flooring(id="f2201", type_id=hybrid_type.id, subtype="SPB Bamboo", colour="Soho", specification_id=hybrid_bamboo_specification.id, price=137.50, discount=0.85, image="f2201.png")
    hybrid_flooring3 = Flooring(id="f2301", type_id=hybrid_type.id, subtype="SPC", colour="Black Butt", specification_id=hybrid_SPC_specification.id, price=97.00, discount=1, image="f2301.png")

    laminate_flooring1 = Flooring(id="f3101", type_id=laminate_type.id, subtype="Laminate AC4", colour="Santos", specification_id=laminate_specification.id, price=55.50, discount=1, image="f3101.png")
    laminate_flooring2 = Flooring(id="f3102", type_id=laminate_type.id, subtype="Laminate AC4", colour="Euro Oak", specification_id=laminate_specification.id, price=55.50, discount=0.85, image="f3102.png")

    vinyl_flooring1 = Flooring(id="f4101", type_id=vinyl_type.id, subtype="Vinyl Planks", colour="Baltic Grey", specification_id=vinyl_specification.id, price=145.00, discount=0.7, image="f4101.png")
    vinyl_flooring2 = Flooring(id="f4102", type_id=vinyl_type.id, subtype="Vinyl Planks", colour="Grand Oak", specification_id=vinyl_specification.id, price=145.00, discount=1, image="f4102.png")

    tile_flooring1 = Flooring(id="f5101", type_id=tile_type.id, subtype="Tile", colour="Beige Concrete", specification_id=tile_600_specification.id, price=88.50, discount=1, image="f5101.png")
    tile_flooring2 = Flooring(id="f5102", type_id=tile_type.id, subtype="Tile", colour="Grey Stone", specification_id=tile_600_specification.id, price=88.50, discount=1, image="f5102.png")
    tile_flooring3 = Flooring(id="f5103", type_id=tile_type.id, subtype="Tile", colour="Calacatta Marble", specification_id=tile_600_specification.id, price=88.50, discount=0.8, image="f5103.png")
    tile_flooring4 = Flooring(id="f5201", type_id=tile_type.id, subtype="Tile", colour="Beige Stone", specification_id=tile_800_specification.id, price=110.50, discount=1, image="f5201.png")
    tile_flooring5 = Flooring(id="f5202", type_id=tile_type.id, subtype="Tile", colour="Charcoal Concrete", specification_id=tile_800_specification.id, price=110.50, discount=0.6, image="f5202.png")


    natural_project_photo_1 = ProjectPhoto(image='p101.png', type_id='ft01')
    natural_project_photo_2 = ProjectPhoto(image='p102.png', type_id='ft01')
    natural_project_photo_3 = ProjectPhoto(image='p103.png', type_id='ft01')
    natural_project_photo_4 = ProjectPhoto(image='p104.png', type_id='ft01')
    natural_project_photo_5 = ProjectPhoto(image='p105.png', type_id='ft01')

    hybrid_project_photo_1 = ProjectPhoto(image='p201.png', type_id='ft02')
    hybrid_project_photo_2 = ProjectPhoto(image='p202.png', type_id='ft02')

    laminate_project_photo_1 = ProjectPhoto(image='p301.png', type_id='ft03')
    laminate_project_photo_2 = ProjectPhoto(image='p302.png', type_id='ft03')

    vinyl_project_photo_1 = ProjectPhoto(image='p401.png', type_id='ft04')
    vinyl_project_photo_2 = ProjectPhoto(image='p402.png', type_id='ft04')

    tile_project_photo_1 = ProjectPhoto(image='p501.png', type_id='ft05')
    tile_project_photo_2 = ProjectPhoto(image='p502.png', type_id='ft05')
    tile_project_photo_3 = ProjectPhoto(image='p503.png', type_id='ft05')

    try:
        db.session.add(natural_project_photo_1)
        db.session.add(natural_project_photo_2)
        db.session.add(natural_project_photo_3)
        db.session.add(natural_project_photo_4)
        db.session.add(natural_project_photo_5)

        db.session.add(hybrid_project_photo_1)
        db.session.add(hybrid_project_photo_2)

        db.session.add(laminate_project_photo_1)
        db.session.add(laminate_project_photo_2)

        db.session.add(vinyl_project_photo_1)
        db.session.add(vinyl_project_photo_2)

        db.session.add(tile_project_photo_1)
        db.session.add(tile_project_photo_2)
        db.session.add(tile_project_photo_3)

        db.session.commit()
    except:
        return 'There was an issue adding the projectPhotos in dbseed function'
    
    natural_project_photos = [natural_project_photo_1, natural_project_photo_2, natural_project_photo_3, natural_project_photo_4, natural_project_photo_5]
    natural_flooring1.project_photos.extend(natural_project_photos)
    natural_flooring2.project_photos.extend(natural_project_photos)
    natural_flooring3.project_photos.extend(natural_project_photos)
    natural_flooring4.project_photos.extend(natural_project_photos)
    natural_flooring5.project_photos.extend(natural_project_photos)

    hybrid_project_photos = [hybrid_project_photo_1, hybrid_project_photo_2]
    hybrid_flooring1.project_photos.extend(hybrid_project_photos)
    hybrid_flooring2.project_photos.extend(hybrid_project_photos)
    hybrid_flooring3.project_photos.extend(hybrid_project_photos)

    laminate_project_photos = [laminate_project_photo_1, laminate_project_photo_2]
    laminate_flooring1.project_photos.extend(laminate_project_photos)
    laminate_flooring2.project_photos.extend(laminate_project_photos)

    vinyl_project_photos = [vinyl_project_photo_1, vinyl_project_photo_2]
    vinyl_flooring1.project_photos.extend(vinyl_project_photos)
    vinyl_flooring2.project_photos.extend(vinyl_project_photos)

    tile_project_photos = [tile_project_photo_1, tile_project_photo_2, tile_project_photo_3]
    tile_flooring1.project_photos.extend(tile_project_photos)
    tile_flooring2.project_photos.extend(tile_project_photos)
    tile_flooring3.project_photos.extend(tile_project_photos)
    tile_flooring4.project_photos.extend(tile_project_photos)
    tile_flooring5.project_photos.extend(tile_project_photos)

    try:
        db.session.add(natural_flooring1)
        db.session.add(natural_flooring2)
        db.session.add(natural_flooring3)
        db.session.add(natural_flooring4)
        db.session.add(natural_flooring5)

        db.session.add(hybrid_flooring1)
        db.session.add(hybrid_flooring2)
        db.session.add(hybrid_flooring3)

        db.session.add(laminate_flooring1)
        db.session.add(laminate_flooring2)

        db.session.add(vinyl_flooring1)
        db.session.add(vinyl_flooring2)

        db.session.add(tile_flooring1)
        db.session.add(tile_flooring2)
        db.session.add(tile_flooring3)
        db.session.add(tile_flooring4)
        db.session.add(tile_flooring5)

        db.session.commit()
    except:
        return 'There was an issue adding the floorings in dbseed function'
    
    return 'DATA LOADED'    