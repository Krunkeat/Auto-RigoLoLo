# Auto-RigoLoLo
###### simple Biped Auto-Rig for Maya 


Support: Create Control, Add Group, Create Limb tool(Biped), Create Reverse Foot n Loc,
        Create Switcher, Mirror Reverse Foot Loc, Create Parent Space, Spine( adaptative jnt), Create Ribbons

Use PySide2 and shiboken2. install via pip if you haven't
pip install PySide2 

WIP: --

To add: color ctrl palette
        switcher link to Hand Meta
                n Foot fk toes
            

To run in maya : 

        import Auto_RigoLoLo
        importlib.reload(Auto_RigoLoLo)

        if __name__ == "__main__":
                try:
                    ui.deleteLater()
                except:
                    pass
                ui = Auto_RigoLoLo.AutoRigOLolo()

                try:
                    ui.show()
                except:
                    ui.deleteLater()

