import CubeGrabbingWorld as cgw
import CubeFightingWorld as cfw
import thread

def main():
    filename = ''
    while filename != 'quit':
        try:
            filename = input('>')
            cgw.showReplay('noteworthy/' + filename)
        except IOError as e:
            try:
                cfw.showReplay('noteworthy/' + filename)
            except IOError as f:
                try:
                    cgw.showReplay(filename)
                except IOError as g:
                    try:
                        cfw.showReplay(filename)
                    except IOError as h:
                        print("Couldn't find file " + filename)
        except SyntaxError:
            print("Use quotes!")
        except NameError:
            print("Use quotes!")
main()
