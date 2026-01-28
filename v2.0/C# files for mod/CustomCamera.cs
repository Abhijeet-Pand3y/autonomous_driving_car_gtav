using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using GTA;
using GTA.Math;
using GTA.Native;
using GTA.NaturalMotion;


namespace ClassLibrary1
{
    internal class CustomCamera : Script
    {
        //static Camera FCamera;
        //static GameplayCamera GFCamera;

        public CustomCamera()
        {
            Tick += OnTick;
            KeyDown += OnKeyDown;
        }

        //public static Vector3 GetRotation(Vector3 curr_rot)
        //{
        //    Vector3 new_rot = curr_rot;



        //    return new_rot;
        //}

        public void CreateCamera()
        {

        }

        public static void UpdateFOV()
        {
            //Vector3 pos = GameplayCamera.Position;
            //Vector3 rot = GameplayCamera.Rotation;

            //float fov = 130.0f;
            //Camera camera = World.CreateCamera(pos, rot, fov);

            //Ped playerPed = Game.Player.Character;
            //Vehicle vehicle = playerPed.CurrentVehicle;

            //Vector3 offset = new Vector3(0.0f, 5.0f, 5.0f);
            //Entity en = Game.Player.Character;

            ////Function.Call(Hash.ATTACH_CAM_TO_ENTITY, camera, en, 0.0f, 1.0f, 1.0f, true);

            //Vector3 entityPosition = en.Position;
            //Vector3 entityRotation = en.Rotation;

            //Function.Call(Hash.SET_CAM_COORD, camera, entityPosition.X, entityPosition.Y, entityPosition.Z);
            //Function.Call(Hash.SET_CAM_ROT, camera, entityRotation.X, entityRotation.Y, entityRotation.Z, 2);

            //World.RenderingCamera = camera;

            Camera camera = Function.Call<Camera>(Hash.GET_RENDERING_CAM);
            
            Entity en = Game.Player.Character;

            Vector3 entityPosition = en.Position;
            Vector3 entityRotation = en.Rotation;
            float x = entityPosition.X;
            float y = entityPosition.Y;
            float z = entityPosition.Z + 1.5f;
            Function.Call(Hash.SET_CAM_COORD, camera, x, y, z);
            Function.Call(Hash.SET_CAM_ROT, camera, entityRotation.X, entityRotation.Y, entityRotation.Z, 2);
            
        }

        public static void CreateCustomCamera(Boolean ren, float fov)
        {
            if (ren)
            {
                Entity en = Game.Player.Character;
                Vector3 entityPosition = en.Position;
                Vector3 entityRotation = en.Rotation;
                //Camera camera = Function.Call<Camera>(Hash.CREATE_CAMERA_WITH_PARAMS, "DEFAULT_SCRIPTED_CAMERA", entityPosition.X, entityPosition.Y, entityPosition.Z, entityRotation.X, entityRotation.Y, entityRotation.Z, 130.0f,true, 2);
                //Function.Call(Hash.RENDER_SCRIPT_CAMS, ren, 1, 10, true, true);
                Camera camera = World.CreateCamera(entityPosition, entityRotation, fov);
                World.RenderingCamera = camera;
            }
            else
            {
                Entity en = Game.Player.Character;
                Vector3 entityPosition = en.Position;
                Vector3 entityRotation = en.Rotation;
                //Camera camera = Function.Call<Camera>(Hash.CREATE_CAMERA_WITH_PARAMS, "DEFAULT_SCRIPTED_CAMERA", entityPosition.X, entityPosition.Y, entityPosition.Z, entityRotation.X, entityRotation.Y, entityRotation.Z, 130.0f,true, 2);
                //Function.Call(Hash.RENDER_SCRIPT_CAMS, ren, 1, 10, true, true);
                Camera camera = World.CreateCamera(entityPosition, entityRotation, fov);
                World.RenderingCamera = camera;
            }
            
        }
        public void OnTick(object sender, EventArgs e)
        {
            try
            {
                UpdateFOV();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }

        public void OnKeyDown(object sender, KeyEventArgs e)
        {
            if(e.KeyCode == Keys.NumPad7)
            {
                try
                {
                    CreateCustomCamera(true, 90.0f);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.ToString());
                }
                
            }
            else if(e.KeyCode == Keys.NumPad9)
            {
                try
                {
                    CreateCustomCamera(false, 100.0f);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.ToString());
                }
            }
        }
    }
}
