from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.task.Task import TaskManager
from typing import Callable 
from CollideObjectBase import *
from direct.gui.OnscreenImage import OnscreenImage

class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, render: NodePath, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3 (0,0,0), 1.2)
        
        # Load the model
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        # Set texture
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
        self.loader = loader
        self.render = render

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, render: NodePath, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName,Vec3 (0, 0, 0), 1.2)
        
        # Load the model
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        # Set texture
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        # Set modelNode as the universe
        
        self.loader = loader
        self.render = render

class Spaceship(SphereCollideObject):# / player
    def __init__(self, loader: Loader, render: NodePath, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, taskManager: TaskManager, accept: Callable[[str, Callable], None]):
        super(Spaceship,self).__init__(loader, modelPath, parentNode, nodeName, Vec3 (0, 0, 0), 1)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.taskManager = taskManager
        self.loader = loader
        self.render = render
        self.accept = accept

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        #self.modelNode.setP(100)

        self.setKeyBindings()
        
    def Thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrust, 'Forward-thrust')
        else: 
            self.taskManager.remove('Forward-thrust')

    def ApplyThrust(self, task):
        rate = 5
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
        
    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLeftTurn, 'LeftTurn')
        else: 
            self.taskManager.remove('LeftTurn')

    def ApplyLeftTurn(self, task):
        # Half a degree every frame
        rate = 0.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
        
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRightTurn, 'RightTurn')
        else:
            self.taskManager.remove('RightTurn')

    def ApplyRightTurn(self, task):
        # Half a degree every frame
        rate = 0.5  
        self.modelNode.setH(self.modelNode.getH() - rate)  
        return Task.cont
        
    def PitchForwd(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyPitchForwd, 'PitchForwd')
        else: 
            self.taskManager.remove('PitchForwd')

    def ApplyPitchForwd(self, task):
        # Half a degree every frame
        rate = 0.5  
        self.modelNode.setP(self.modelNode.getP() + rate)  
        return Task.cont
        
    def PitchBack(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyPitchBack, 'PitchBack')
        else: 
            self.taskManager.remove('PitchBack')

    def ApplyPitchBack(self, task):
        # Half a degree every frame
        rate = 0.5  
        self.modelNode.setP(self.modelNode.getP() - rate) 
        return Task.cont
        
    def RollLeft(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollLeft, 'RollLeft')
        else: 
            self.taskManager.remove('RollLeft')

    def ApplyRollLeft(self, task):
        # Half a degree every frame
        rate = 0.5  
        self.modelNode.setR(self.modelNode.getR() - rate)  
        return Task.cont

    def RollRight(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollRight, 'RollRight')
        else:
            self.taskManager.remove('RollRight')

    def ApplyRollRight(self, task):
        # Half a degree every frame
        rate = 0.5  
        self.modelNode.setR(self.modelNode.getR() + rate) 
        return Task.cont

    
    def Fire(self):
        if self.missileBay:
            travRate = self.missileDistance
            aim = self.render.getRelativePoint(self.modelNode, Vec3.forward())
            aim.normalize()
            fireSolution = aim * travRate
            inFront =aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag = 'Missile' + str(Missile.missileCount)
            posVec = self.modelNode.getPos() + inFront
            currentMissile = Missile(self.loader, './Assets/Phaser/Phaser.egg', self.render, tag, posVec, 4.0)
            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fuid = 1)
            Missile.Intervals[tag].staret()

        else:
            if not self.taskManager.hasTaskNamd('reloaad'):
                print('Initializing reload...')
                self.taskManager.doMethodLater(0,self.Reload, 'reload')
                return Task.cont
            
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
        
            if self.missileBay > 1:
                self.missileBay = 1

            print("Reload complete")
            return Task.done
        
        elif task.time <= self.reloadTime:
            print("Reload proceeding...")
            return Task.cont
           
    def setKeyBindings(self):  
        # All key Bindings for Spaceship move
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])

        # Keys for left and right
        self.accept('arrow_left', self.LeftTurn, [1])
        self.accept('arrow_left-up', self.LeftTurn, [0])
        self.accept('arrow_right', self.RightTurn, [1])
        self.accept('arrow_right-up', self.RightTurn, [0])

        # Keys for up and down
        self.accept('arrow_up', self.PitchForwd, [1])
        self.accept('arrow_up-up', self.PitchForwd, [0])
        self.accept('arrow_down', self.PitchBack, [1])
        self.accept('arrow_down-up', self.PitchBack, [0])

        # Keys for rotating left and right
        self.accept('a', self.RollLeft, [1])
        self.accept('a-up', self.RollLeft, [0])
        self.accept('d', self.RollRight, [1])
        self.accept('d-up', self.RollRight, [0])

        #f to fire 
        self.accept('f', self.Fire)

    def checkIntervals(self, task):
        for i in Missile.Intervals:
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
            del Missile.Intervals[i]
            del Missile.fireModels[i]
            del Missile.cNodes[i]
            del Missile.collisionSolids[i]

            print(1 + 'has reached the end of it fire solution.')
            break
            return Task.cont
        
    def EnableHud(self):
        self.Hud = OnscreenImage(image = "./Assets/Hud/Reticle3b.png", pos = Vec3 (0,0,0), scale = 0.1)
        self.hud.setTransparency(TransparencyAttrib.MAlpha)
        self.EnableHUd()

      
class SpaceStation(CollisionCapsuleObject):
    def __init__(self, loader: Loader, render: NodePath, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, radius: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName,1, -1, 5, 1, -1, -5, 0)

        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.loader = loader
        self.render = render
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
        #self.station = loader.loadModel("./Assets/SpaceStation1B/spaceStation.x")

class Missile(SphereCollideObject):

    fireModels ={}
    cNodes = {}
    collisionSolids = {}
    Intervals = {}
    missileCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1):
        super(Missile, self).__init__(Loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)
        self.modelNode.setName(nodeName)

        Missile.missileCount += 1

        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName]=self.collisionNode
        Missile.collisionSolids[nodeName] = self.collisionNode.node().getsolid(0)
        Missile.cNodes[nodeName].show()

        print("Fire torpedo #" + str(Missile.missileCount))

class DroneShowBase(SphereCollideObject):
    def DrawCloudDefense(self, loader: Loader, render: NodePath, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float,centralObject, droneName, position):
        super(DroneShowBase, self).__init__(loader, modelPath, parentNode, nodeName, Vec3 (0,0,0), 1.2)


        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
        self.loader = loader
        self.render = render

        """"
        placeholder = self.render.attachNewNode('placeholder')
        placeholder.setPos(position)

        drone_model = self.loader.loadModel("Assets/DroneDefender/DroneDefender.obj")
        drone_model.reparentTo(placeholder)
        drone_model.setScale(3)
"""
    # # of Drone
    droneCount = 0