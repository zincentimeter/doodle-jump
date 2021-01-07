using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.IO;
public class positionGet : MonoBehaviour
{
    private string Buffer = "";
    private GameObject[] m_Desk;
    public Player_Controller player;
    public Text text;
    public GameObject Camera;
	public Dictionary<String, String> Storage;

	public Component Connection;
    // Use this for initialization
    void Start()
    {
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
		Storage["is_died"] = "False";
		Storage["score"] = $"{text.text}";

		var Output = "";
		foreach (var entry in Storage)
		{
			Output += $"\'{entry.Key}\' : {entry.Value},";
		}
		Output = "{" + Output + "}";
		Connection.GetComponent<Communicate_Python>().ServerRequest(Output);
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
}
