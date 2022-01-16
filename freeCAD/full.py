from FreeCAD import Base
import Part,PartGui
import PartDesignGui
import Sketcher


import FreeCAD
import PartDesign


import math
import os
import winsound
import time

duration = 1000  # millisecond
freq = 440  # Hz

# = = = = = = = = = = = = = = = = = = = = =
L1 = 82.0
L2 = 80.0

l1 = L1 / 2.
l2 = L2 / 2.

DD = 44
rr = DD / 2.

bigR = 150.
smlR = 250.


X1 = 58.
x1 = X1 / 2.

Y1 = 50.
y1 = Y1 / 2.

# = = = = = = = = = = = = = = = = = = = = =
def base( AS ):
    print( "base" )
    T1 = Base.Vector( - l1,  l2, 0.  )
    T2 = Base.Vector( - l1, -l2, 0. )
    T3 = Base.Vector(   l1, -l2, 0. )
    T4 = Base.Vector(   l1,  l2, 0. )

    ls0 = Part.LineSegment( T2, T1 )
    gm0 = AS.addGeometry( ls0, False)
    AS.addConstraint( Sketcher.Constraint('DistanceY', gm0, L2) ) 

    ls1 = Part.LineSegment( T2, T3 )
    gm1 = AS.addGeometry( ls1, False)
    AS.addConstraint( Sketcher.Constraint('DistanceX', gm1, L1) ) 


    ls2 = Part.LineSegment( T3, T4 )
    gm2 = AS.addGeometry( ls2, False)
    AS.addConstraint( Sketcher.Constraint('DistanceY', gm2, L2) ) 

    ls3 = Part.LineSegment( T4, T1 )
    gm3 = AS.addGeometry( ls3, False)
    AS.addConstraint( Sketcher.Constraint('DistanceX', gm3, L1) ) 


    AS.addConstraint( Sketcher.Constraint('Coincident', gm0, 1, gm1, 1))
    AS.addConstraint( Sketcher.Constraint('Coincident', gm1, 2, gm2, 1))
    AS.addConstraint( Sketcher.Constraint('Coincident', gm2, 2, gm3, 2))
    AS.addConstraint( Sketcher.Constraint('Coincident', gm3, 1, gm0, 2))

    AS.addConstraint( Sketcher.Constraint('Symmetric', gm0, 1, gm0, 2, -1) ) # -1 denotes the horizontal x axis
    AS.addConstraint( Sketcher.Constraint('Symmetric', gm1, 1, gm1, 2, -2) ) # -2 denotes the vertical   y axis


    AS.addGeometry( Part.Circle( App.Vector(0., 0., 0. ), App.Vector(0,0,1), rr ), False )
    AS.addConstraint( Sketcher.Constraint('Radius', 4, rr)) 



#    AS.addConstraint(Sketcher.Constraint('Coincident',4,3,-1,1)) 
#    AS.setDatum(10,App.Units.Quantity( rr +' mm'))
    Gui.SendMsgToActiveView("ViewFit")

# end def base
# = = = = = = = = = = = = = = = = = = = = =
def plate( ):
    print( "plate" )
    f = AD.addObject('Part::Extrusion','Extrude')
    f.Base = AD.getObject('Sketch')
    f.DirMode = "Normal"
    f.DirLink = None
    f.LengthFwd = 1.5
    f.LengthRev = 0.
    f.Solid = True
    f.Reversed = False
    f.Symmetric = False
    f.TaperAngle    = 0.
    f.TaperAngleRev = 0.
    Gui.SendMsgToActiveView("ViewFit")

# end def plate
# = = = = = = = = = = = = = = = = = = = = = 
def wll( AS, offsetX, offsetY, cLENGTH, cHEIGHT, cPTR ):
    print( "wll" )
    P1 = Base.Vector( 0. - cLENGTH, cHEIGHT, 0.  )
    P2 = Base.Vector( 0. - cLENGTH, 0. , 0. )
    P3 = Base.Vector( cLENGTH, 0. , 0. )
    P4 = Base.Vector( cLENGTH, cHEIGHT, 0. )

    C1 = Base.Vector( 0, -cPTR, 0)

    RADIUS = math.hypot ( cHEIGHT + cPTR,  cLENGTH )

    ls0 = Part.LineSegment( P2, P1 )
    gm0 = AS.addGeometry( ls0, False)

    AS.addConstraint( Sketcher.Constraint('Vertical',  gm0) ) 
    AS.addConstraint( Sketcher.Constraint('DistanceY', gm0, cHEIGHT) ) 


    ls1 = Part.LineSegment( P2, P3 )
    gm1 = AS.addGeometry( ls1, False)
#    AS.addConstraint( Sketcher.Constraint('Horizontal', gm1) ) 
    AS.addConstraint( Sketcher.Constraint('DistanceX',  gm1, cLENGTH + cLENGTH) ) 
    AS.addConstraint( Sketcher.Constraint('Symmetric', gm1, 1, gm1, 2, -2) ) # -2 denotes the vertical y axis; -1 denotes the horizontal x axis
    AS.addConstraint(Sketcher.Constraint('Block', gm1 )) 


    ls2 = Part.LineSegment( P3, P4 )
    gm2 = AS.addGeometry( ls2, False)
    AS.addConstraint( Sketcher.Constraint('Vertical',  gm2) ) 
    AS.addConstraint( Sketcher.Constraint('DistanceY', gm2, cHEIGHT) ) 


    AS.addConstraint( Sketcher.Constraint('Coincident', gm0, 1, gm1, 1))
    AS.addConstraint( Sketcher.Constraint('Coincident', gm1, 2, gm2, 1))

    crc = Part.Circle( C1, App.Vector(0,0,1), RADIUS )
    gm3 = AS.addGeometry( Part.ArcOfCircle(  crc, 0.8, math.radians(131.78) ), False)
#    print( math.degrees( 2.3 ) )

#    AS.addConstraint( Sketcher.Constraint('DistanceX', gm3, 3,    0. ) ) 
    AS.addConstraint( Sketcher.Constraint('DistanceY', gm3, 3, -cPTR ) ) 

    AS.addConstraint( Sketcher.Constraint('Coincident', gm0, 2, gm3, 2))
    AS.addConstraint( Sketcher.Constraint('Coincident', gm2, 2, gm3, 1))

    Gui.SendMsgToActiveView("ViewFit")

# end def wll
# - - - - - - - - - - - - - - - - - - - - 
def left( ):
    print( "left" )

    Sketch1 = 'Sketch001'
    SK1 = AB.newObject('Sketcher::SketchObject', Sketch1)

    SK1.Support = ( AD.getObject('YZ_Plane'),[''])
    SK1.MapMode = 'FlatFace'
    AD.recompute()

    wll( SK1, 0., 0., l2, 4. , bigR )

    SK1.AttachmentOffset = App.Placement( App.Vector( 0., 0., -x1 ), App.Rotation(App.Vector(0,0,1), 0) )
#~ ~ ~
    Sketch2 = 'Sketch002'
    SK2 = AB.newObject('Sketcher::SketchObject', Sketch2)

    SK2.Support = ( AD.getObject('YZ_Plane'),[''])
    SK2.MapMode = 'FlatFace'
    AD.recompute()

    wll( SK2, 0., 0., l2, 4. , smlR )
    SK2.AttachmentOffset = App.Placement( App.Vector( 0., 0., -l1 ), App.Rotation(App.Vector(0,0,1), 0) )

    AO = AD.addObject('Part::Loft','Loft')
    AO.Sections=[ SK1, SK2, ]
    AO.Solid=True
    AO.Ruled=False
    AO.Closed=False

#    SK1.Visibility=False
#    SK2.Visibility=False
#    AO.Visibility=False
    Gui.SendMsgToActiveView("ViewFit")

# end def left
# - - - - - - - - - - - - - - - - - - - - 
def right( ):
    print( "right" )

    Sketch3 = 'Sketch003'
    SK3 = AB.newObject('Sketcher::SketchObject', Sketch3)

    SK3.Support = ( AD.getObject('YZ_Plane'),[''])
    SK3.MapMode = 'FlatFace'
    AD.recompute()

    wll( SK3, 0., 0., l2, 4. , bigR )

    SK3.AttachmentOffset = App.Placement( App.Vector( 0., 0., x1 ), App.Rotation(App.Vector(0,0,1), 0) )
#~ ~ ~
    Sketch4 = 'Sketch004'
    SK4 = AB.newObject('Sketcher::SketchObject', Sketch4)

    SK4.Support = ( AD.getObject('YZ_Plane'),[''])
    SK4.MapMode = 'FlatFace'
    AD.recompute()

    wll( SK4, 0., 0., l2, 4. , smlR )
    SK4.AttachmentOffset = App.Placement( App.Vector( 0., 0., l1 ), App.Rotation(App.Vector(0,0,1), 0) )

    AO = AD.addObject('Part::Loft','Loft')
    AO.Sections=[ SK3, SK4, ]
    AO.Solid=True
    AO.Ruled=False
    AO.Closed=False

#    SK3.Visibility=False
#    SK4.Visibility=False
#    AO.Visibility=False
    Gui.SendMsgToActiveView("ViewFit")


# end def right
# - - - - - - - - - - - - - - - - - - - - 
def up( ):
    print( "up" )

    Sketch5 = 'Sketch005'
    SK5 = AB.newObject('Sketcher::SketchObject', Sketch5)

    SK5.Support = ( AD.getObject('XZ_Plane'),[''])
    SK5.MapMode = 'FlatFace'
    AD.recompute()

    wll( SK5, 0., 0., l1, 4. , smlR )
    SK5.AttachmentOffset = App.Placement( App.Vector( 0., 0., -l2 ), App.Rotation(App.Vector(0,0,1), 0) )
# - - - - - - - - - - - - - - - - - - - - - -
    Sketch6 = 'Sketch006'
    SK6 = AB.newObject('Sketcher::SketchObject', Sketch6)
    SK6.Support = ( AD.getObject('XZ_Plane'),[''])
    SK6.MapMode = 'FlatFace'
    AD.recompute()
    wll( SK6, 0., 0., l1, 4., bigR )
    SK6.AttachmentOffset = App.Placement( App.Vector( 0., 0.,  -y1), App.Rotation(App.Vector(0,0,1), 0) )
# ~ ~ ~ ~ ~
    AO = AD.addObject('Part::Loft','Loft')
    AO.Sections=[ SK5, SK6, ]
    AO.Solid=True
    AO.Ruled=False
    AO.Closed=False

#    SK5.Visibility=False
#    SK6.Visibility=False
#    AO.Visibility=False
    Gui.SendMsgToActiveView("ViewFit")


# end def up
# - - - - - - - - - - - - - - - - - - - - 
def down( ):
    print( "down" )

    Sketch7 = 'Sketch007'
    SK7 = AB.newObject('Sketcher::SketchObject', Sketch7)

    SK7.Support = ( AD.getObject('XZ_Plane'),[''])
    SK7.MapMode = 'FlatFace'
    AD.recompute()

    wll( SK7, 0., 0., l1, 4. , smlR )
    SK7.AttachmentOffset = App.Placement( App.Vector( 0., 0., y1 + 1.5 ), App.Rotation(App.Vector(0,0,1), 0) )# - - - - - - - - - - - - - - - - - - - - - -

    Sketch8 = 'Sketch008'
    SK8 = AB.newObject('Sketcher::SketchObject', Sketch8)
    SK8.Support = ( AD.getObject('XZ_Plane'),[''])
    SK8.MapMode = 'FlatFace'
    AD.recompute()

    wll( SK8, 0., 0., l1, 4., bigR )
    SK8.AttachmentOffset = App.Placement( App.Vector( 0., 0.,  y1 ), App.Rotation(App.Vector(0,0,1), 0) )
# ~ ~ ~ ~ ~
    AO = AD.addObject('Part::Loft','Loft')
    AO.Sections=[ SK7, SK8, ]
    AO.Solid=True
    AO.Ruled=False
    AO.Closed=False

#    SK7.Visibility=False
#    SK8.Visibility=False
#    AO.Visibility=False
    Gui.SendMsgToActiveView("ViewFit")

# end def down
# - - - - - - - - - - - - - - - - - - - - 
def pir( SKp, f, dir ):
    print( "pir" )

    SKp.Support = ( AD.getObject('YZ_Plane'),[''])
    SKp.MapMode = 'FlatFace'
    AD.recompute()

    DS = 12. + 1.
    RS = DS / 2.
    hs = RS + 5.

    dr = 10. + 1.
    rr = dr / 2.

    S1 = Base.Vector( -RS, hs, 0. )
    S2 = Base.Vector( -RS, 0., 0. )
    S3 = Base.Vector(  RS, 0., 0. )
    S4 = Base.Vector(  RS, hs, 0. )

    C1 = Base.Vector( 0, hs, 0)

    ls0 = Part.LineSegment( S2, S1 )
    gm0 = SKp.addGeometry( ls0, False)

    ls1 = Part.LineSegment( S2, S3 )
    gm1 = SKp.addGeometry( ls1, False)


    ls2 = Part.LineSegment( S3, S4 )
    gm2 = SKp.addGeometry( ls2, False)


    SKp.addConstraint( Sketcher.Constraint('Coincident', gm0, 1, gm1, 1))
    SKp.addConstraint( Sketcher.Constraint('Coincident', gm1, 2, gm2, 1))

    SKp.addConstraint( Sketcher.Constraint('Symmetric', gm0, 2, gm2, 2, -2) ) # -2 denotes the vertical   y axis

    SKp.addConstraint( Sketcher.Constraint('Vertical',   gm2) ) 
    SKp.addConstraint( Sketcher.Constraint('DistanceY', gm0, 2, hs) ) 

    gms = SKp.addGeometry( Part.Circle( C1, App.Vector(0,0,1), rr ), False)
    SKp.addConstraint( Sketcher.Constraint('DistanceY', gms, 3, hs) ) 

    gmS = SKp.addGeometry( Part.ArcOfCircle( Part.Circle( C1, App.Vector( 0, 0, 1 ), RS ), 0., math.radians(180.) ), False)
#    print ( math.radians( 180 ) )


    SKp.addConstraint( Sketcher.Constraint('Coincident', gmS, 2, gm0, 2) ) 
    SKp.addConstraint( Sketcher.Constraint('Coincident', gmS, 1, gm2, 2) ) 
    SKp.addConstraint( Sketcher.Constraint('DistanceY',  gmS, 3, hs) ) 


    SKp.addConstraint(Sketcher.Constraint( 'DistanceX',-1,1, gm2,2, RS)) 

    SKp.addConstraint(Sketcher.Constraint('Angle', 1,1, 0,1, math.radians( 80 )))
#    print ( math.radians( 80 ) )
    Gui.SendMsgToActiveView("ViewFit")

#    hole.Placement.Base.x = x
#    hole.Placement.Base.y = y
#prism.Placement=Base.Placement(Base.Vector(0.00,0.00,0.00),Base.Rotation(0.00,0.00,0.00,1.00))
# end def pir

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

AD = App.getDocument('Unnamed')
AB = AD.addObject('PartDesign::Body','Body')

# = = = = = = = = = = = = = = = = = = = = = =

Sketch0 = 'Sketch'
SK0 = AB.newObject('Sketcher::SketchObject', Sketch0)

SK0.Support = ( AD.getObject('XY_Plane'),[''])
SK0.MapMode = 'FlatFace'
AD.recompute()

base( SK0 )
# - - - -

time.sleep(15.5)
left(  )
time.sleep(15.5)
right( )
time.sleep(15.5)
up( )
time.sleep(15.5)
down( )
time.sleep(15.5)
plate( )

Sketch9 = 'Sketch009'
SK9 = AB.newObject('Sketcher::SketchObject', Sketch9)

f = AD.addObject('Part::Extrusion','Extrude')
pir( SK9, f, True )
SK9.AttachmentOffset = App.Placement(App.Vector( -33., 0., -29.), App.Rotation( App.Vector( 1,0,0), 10))

f.Base = SK9
f.DirMode = "Normal"
f.DirLink = None
f.LengthFwd = 2.
f.LengthRev = 0.
f.Solid = True
f.Reversed = True
f.Symmetric = False
f.TaperAngle = 0.
f.TaperAngleRev = 0.

Sketch10 = 'Sketch010'
SK10 = AB.newObject('Sketcher::SketchObject', Sketch10)

f = AD.addObject('Part::Extrusion','Extrude001')

time.sleep(15.5)
pir( SK10, f, False )
SK10.AttachmentOffset = App.Placement(App.Vector( -33., 0., 29.), App.Rotation( App.Vector( 1,0,0), -10))


f.Base = SK10
f.DirMode = "Normal"
f.DirLink = None
f.LengthFwd = 2.
f.LengthRev = 0.
f.Solid = True
f.Reversed = False
f.Symmetric = False
f.TaperAngle = 0.
f.TaperAngleRev = 0.


#SK9.Placement.Base.x = 10.
#SK9.Placement.Base.y = 20.



Gui.SendMsgToActiveView("ViewFit")
winsound.Beep(freq, duration)
time.sleep(5.5)
Gui.SendMsgToActiveView('ViewAxo')

