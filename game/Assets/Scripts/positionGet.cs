using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.IO;
public class positionGet : MonoBehaviour {
	private string log = "";
	private GameObject[] m_Desk;
	public Player_Controller player;
	public Text text;
	// Use this for initialization
	void Start () {
		player = GameObject.Find("Doodler").GetComponent<Player_Controller>();
		text = GameObject.Find ("Text_Score").GetComponent<Text>();
	}
	
	// Update is called once per frame
	void Update () {
		log = "#board ";
		m_Desk = GameObject.FindGameObjectsWithTag ("Object");
		log += m_Desk.Length.ToString ();
		log += "\n";
		for (int i = 0; i < m_Desk.Length; i++) {
			log += m_Desk[i].name;
			log += " ";
			log += m_Desk[i].transform.position.ToString ();
			log += "\n";
		}

		log += "agentPos ";
		log += player.transform.position.ToString ();
		log += "\n";
		log += "agentSpeed ";
		log += player.getSpeed();
		log += "\n";
		log += "score ";
		log += text.text;
		print (log);
		FileStream fs = new FileStream("log.txt", FileMode.Create);
		StreamWriter sw = new StreamWriter(fs);
		sw.Write(log);
		sw.Flush();
		sw.Close();
		fs.Close();
	}
}
