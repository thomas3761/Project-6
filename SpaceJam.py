from direct.showbase.ShowBase import ShowBase
import SpaceJamClasses as spaceJamClasses
import DefensePaths as defensePaths
from panda3d.core import *
import math, random
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from CollideObjectBase import PlacedObject

class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setScene()
        
        self.planet1 = spaceJamClasses.Planet(self.loader, self.render, "./Assets/Planets/protoPlanet.x", self.render, "Planet1", "./Assets/Planets/Planet 1.jpg", Vec3(150, 5000, 67), 350)
        self.planet2 = spaceJamClasses.Planet(self.loader, self.render, "./Assets/Planets/protoPlanet.x", self.render, "Planet2", "./Assets/Planets/Planet 2.jpg", Vec3(5314, 1274, 976), 350)
        self.planet3 = spaceJamClasses.Planet(self.loader, self.render, "./Assets/Planets/protoPlanet.x", self.render, "Planet3", "./Assets/Planets/Planet 3.png", Vec3(1985, 1274, 1112), 350)
        self.planet4 = spaceJamClasses.Planet(self.loader, self.render, "./Assets/Planets/protoPlanet.x", self.render, "Planet4", "./Assets/Planets/Planet 4.jpg", Vec3(3067, 1274, 2378), 350)
        self.planet5 = spaceJamClasses.Planet(self.loader, self.render, "./Assets/Planets/protoPlanet.x", self.render, "Planet5", "./Assets/Planets/Planet 5.jpg", Vec3(1382, 1274, 4567), 350)
        self.planet6 = spaceJamClasses.Planet(self.loader, self.render, "./Assets/Planets/protoPlanet.x", self.render, "Planet6", "./Assets/Planets/Planet 6.png", Vec3(4502, 1274, 6478), 350)

        self.Spaceship = spaceJamClasses.Spaceship(self.loader, self.render, "./Assets/Dumbledore/Dumbledore.egg", self.render, "Spaceship", "./Assets/Dumbledore/spacejet_C.png", Vec3(0, 0, 0), 10, self.taskMgr, self.accept, self.cTrav)

        self.universe = spaceJamClasses.Universe(self.loader, self.render, "./Assets/Universe/Universe.x", self.render, "Universe", "./Assets/Universe/space-galaxy.jpg", Vec3(0,0,0), 15000) 

        self.spaceStation = spaceJamClasses.SpaceStation(self.loader, self.render, "./Assets/SpaceStation1B/spaceStation.x", self.render, "SpaceStation", "./Assets/SpaceStation1B/SpaceStation1_Dif2.png", Vec3(1000, 5000, 80), Vec3(10, 10, 50), 5)

        self.droneshowbase = spaceJamClasses.DroneShowBase(self.loader, self.render, "./Assets/DroneDefender/DroneDefender.obj", self.render, "DroneObject", "./Assets/DroneDefender/octotoad1_auv.png", Vec3(0, 0, 0), 1.0)

        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.cTrav.traverse(self.render)
        self.pusher.addCollider(self.Spaceship.collisionNode, self.Spaceship.modelNode)
        self.cTrav.addCollider(self.Spaceship.collisionNode,self.pusher)
        self.cTrav.showCollisions(self.render)


        fullCycle = 60
        for j in range(fullCycle):
            spaceJamClasses.DroneShowBase.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.DroneShowBase.droneCount)
            self.DrawBaseballSeams(self.planet1, 10, 36)
            #position = Vec3(0, 0, 0) this bricks Circle
        
        
        self.DrawCircleXYDefense()
        self.DrawCircleXZDefense()
        self.DrawCircleYZDefense()

        

        #self.SetCamera()

    def DrawCircleXYDefense(self):
        self.parent = self.loader.loadModel('./Assets/DroneDefender/DroneDefender.obj')
        self.parent.setScale(0.25)
        a = 0.0
        aInc = 0.2
        R = 50.0

        for i in range(30):
            posVec = (R * math.cos(a), R * math.sin(a), 0)
            self.placeholder = self.render.attachNewNode("Placeholder")
            self.placeholder.setPos(posVec)
            self.placeholder.setColor(255, 0, 0, 1)
            self.parent.instanceTo(self.placeholder)
            a += aInc

    def DrawCircleXZDefense(self):
        self.parent = self.loader.loadModel('./Assets/DroneDefender/DroneDefender.obj')
        self.parent.setScale(0.25)
        a = 0.0
        aInc = 0.2
        R = 50.0

        for i in range(30):
            posVec = (R * math.cos(a), 0, R * math.sin(a))
            self.placeholder = self.render.attachNewNode("Placeholder")
            self.placeholder.setPos(posVec)
            self.placeholder.setColor(0, 255, 0, 1)
            self.parent.instanceTo(self.placeholder)
            a += aInc

    def DrawCircleYZDefense(self):
        self.parent = self.loader.loadModel('./Assets/DroneDefender/DroneDefender.obj')
        self.parent.setScale(0.25)
        a = 0.0
        aInc = 0.2
        R = 50.0

        for i in range(30):
            posVec = (0, R * math.cos(a), R * math.sin(a))
            self.placeholder = self.render.attachNewNode("Placeholder")
            self.placeholder.setPos(posVec)
            self.placeholder.setColor(0, 0, 255, 1)
            self.parent.instanceTo(self.placeholder)
            a += aInc

    def DrawBaseballSeams(self, centralObject, step, numSeams, radius=1): 
        for i in range(numSeams):
            position = defensePaths.BaseballSeams(step, numSeams, B=0.4) * radius
            SpaceJamClasses.droneShowBase(self.loader, self.render, "./Assets/DroneDefender/DroneDefender.obj", self.render, "DroneObject", "./Assets/DroneDefender/octotoad1_auv.png", Vec3(0, 0, 0), 1.0, centralObject, f"Drone_{i}", position)
        
    
    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Spaceship.modelNode)
        self.camera.setFluidPos(0, 1, 0)

    def setScene(self):
        return

app = SpaceJam()
app.run()