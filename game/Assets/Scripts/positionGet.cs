using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
public class positionGet : MonoBehaviour {
	private string log = "";
	private GameObject[] m_Desk;
	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		log = DateTime.Now.TimeOfDay.ToString();
		log += "\n";
		m_Desk = GameObject.FindGameObjectsWithTag ("Object");
		for (int i = 0; i < m_Desk.Length; i++) {
			log += m_Desk[i].name;
			log += " ";
			log += m_Desk[i].transform.position.ToString ();
			log += "\n";
		}
		GameObject player = GameObject.FindGameObjectsWithTag ("Player") [0];
		log += "Player ";
		log += player.transform.position.ToString ();
		print (log);
		FileStream fs = new FileStream("log.txt", FileMode.Create);
		StreamWriter sw = new StreamWriter(fs);
		sw.Write(log);
		sw.Flush();
		sw.Close();
		fs.Close();
	}
}
