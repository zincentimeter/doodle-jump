using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.IO;
using Newtonsoft.Json;
public class positionGet : MonoBehaviour
{
    private string Buffer = "";
    private GameObject[] m_Desk;
    public Player_Controller player;
    public Text text;
    public GameObject Camera;
	public Dictionary<String, String> Storage;
    private GameObject Game_Controller;
	public Component Connection;
    // Use this for initialization
    void Start()
    {
        Game_Controller = GameObject.Find("Game_Controller");
        player = GameObject.Find("Doodler").GetComponent<Player_Controller>();
        text = GameObject.Find("Text_Score").GetComponent<Text>();
        Camera = GameObject.Find("Main Camera");
		Storage = new Dictionary<String, String>();
		Connection = gameObject.AddComponent(typeof(Communicate_Python));
		// Connection.GetComponent<Communicate_Python>().Start();
    }

    // Update is called once per frame
    void Update()
    {
		m_Desk = GameObject.FindGameObjectsWithTag ("Object");
		var agent_pos_x = player.transform.position.x.ToString();
		var agent_pos_y = player.transform.position.y.ToString();
		Storage["agent_pos"] = $"({agent_pos_x},{agent_pos_y})";
		Storage["agent_speed"] = $"{player.getSpeed()}";
		Storage["num_boards"] = $"{m_Desk.Length}";
		var raw_boards = "";
        for (int i = 0; i < m_Desk.Length; i++) {
        	var type = GetBoardTypeValue(m_Desk[i].name);
			var x = m_Desk[i].transform.position.x;
			var y = m_Desk[i].transform.position.y;
			raw_boards += $"(({x},{y}),{type}),";
        }
		raw_boards = "[" + raw_boards + "]";
		Storage["raw_boards"] = raw_boards;
		Storage["is_pause"] = "False";
		Storage["is_died"] = Game_Controller.GetComponent<Game_Controller>().Get_GameOver() ? "True" : "False";
		Storage["is_hit"] = player.Hit ? "True" : "False";
		Storage["score"] = $"{text.text}";

		var Output = "";
		foreach (var entry in Storage)
		{
			Output += $"\'{entry.Key}\' : {entry.Value},";
		}
		Output = "{" + Output + "}";

		String ReceivedMessage = Connection.GetComponent<Communicate_Python>().ServerRequest(Output);
		if (ReceivedMessage == "0")
			return;
		// String[] Messages = ReceivedMessage.Split( "|".ToCharArray(), StringSplitOptions.RemoveEmptyEntries );
		// if (Messages.Length == 2)
		// {
		// 	// // print(Messages[1].Trim(' ').TrimStart('{').TrimEnd('}').Replace('\'', '\"'));
		// 	// var Dict = JsonConvert.DeserializeObject<Dictionary<String, float>>(Messages[1]);
			
		// 	// // String[] Q_Messages = Messages[1] .Trim(charsToTrim) .Split( ",".ToCharArray(), StringSplitOptions.RemoveEmptyEntries );
		// 	// // List<GameObject> UItext = new List<GameObject>();
		// 	// foreach (var entry in Dict)
		// 	// {
		// 	// 	// print(entry);
		// 	// 	var Coordinates = entry.Key.Trim(' ').TrimStart('(').TrimEnd(')').Split(',');
		// 	// 	float Q_Value = entry.Value;
		// 	// 	float x = float.Parse(Coordinates[0]);
		// 	// 	float y = float.Parse(Coordinates[1]);


		// 	// 	print($"{x} {y} {Q_Value}");
		// 	// 	GameObject Object = new GameObject($"({x},{y})");
		// 	// 	// RectTransform trans = Object.AddComponent<RectTransform>();
		// 	//     // trans.anchoredPosition = new Vector2(x, y);
		// 	// 	// Text TextBox = Object.AddComponent<Text>();
		// 	// 	// TextBox.text = Q_Value.ToString();
		// 	// 	// TextBox.fontSize = 80;
		// 	// 	// TextBox.color = Color.green;
		// 	// 	// TextBox.transform.position = new Vector3(x, y, 0);
		// 	// 	// TextBox.rectTransform.anchoredPosition3D = new Vector3(x, y, 0);
		// 	// 	// Object.transform.SetParent(GameObject.Find("Main Camera").transform);
		// 	// 	// UItext.Add(Object);
		// 	// 	// Object.transform.SetParent(null);
		// 	// }

		// }
		String[] DirectionMessages = ReceivedMessage.Split(' ');
		// print($"Recv:{ReceivedMessage}");
		int control = int.Parse(DirectionMessages[0]);
		float destinationX = float.Parse(DirectionMessages[1]);
		float destinationY = float.Parse(DirectionMessages[2]);

		// print(Player.ToString());
		player.SetDirection(control, destinationX, destinationY);
		// Connection.ServerRequest(Output);
		// Storage.Add("agent_pos", $"({agent_pos_x},{agent_pos_y})");
		// Storage.Add("agent_speed", $"{player.getSpeed()}");
		// Storage.Add("num_boards", $"{m_Desk.Length}");
        // log = "#board ";
        // m_Desk = GameObject.FindGameObjectsWithTag ("Object");
        // log += m_Desk.Length.ToString ();
        // log += "\n";
		// Storage.Add("raw_boards", raw_boards);
		// Storage.Add("is_pause", "False");
		// Storage.Add("is_died", "False");
		// Storage.Add("score", $"{text.text}");
		// foreach (var item in Storage)
		// {
		// 	// Console.WriteLine(item.ToString());
		// 	print(item.ToString());
		// }
        // log += "agentPos ";
        // log += player.transform.position.ToString ();
        // log += "\n";
        // log += "agentSpeed ";
        // log += player.getSpeed();
        // log += "\n";
        // log += "score ";
        // log += text.text;
        // log += "\n";
        // log += "Camera ";
        // log += Camera.transform.position.y.ToString ();
        // FileStream fs = new FileStream("logout.txt", FileMode.Create);
        // StreamWriter sw = new StreamWriter(fs);
        // sw.Write(log);
        // sw.Flush();
        // sw.Close();
        // fs.Close();
    }



	int GetBoardTypeValue(String BoardType)
	{
		switch (BoardType)
		{
			case "Platform_Green":
				return 0;
			case "Platform_Brown":
				return 1;
			case "Platform_Blue":
				return 2;
			case "Platform_White":
				return 3;
			case "Propeller":
				return 4;
			case "Trampoline":
				return 5;
			case "Spring":
				return 6;
			default:
				return -1;
		}
	}

	GameObject CreateText(Transform canvas_transform, float x, float y, string text_to_print, int font_size, Color text_color)
	{
		GameObject UItextGO = new GameObject("Text2");
		UItextGO.transform.SetParent(canvas_transform);

		RectTransform trans = UItextGO.AddComponent<RectTransform>();
		trans.anchoredPosition = new Vector2(x, y);

		Text text = UItextGO.AddComponent<Text>();
		text.text = text_to_print;
		text.fontSize = font_size;
		text.color = text_color;

		return UItextGO;
	}
}
