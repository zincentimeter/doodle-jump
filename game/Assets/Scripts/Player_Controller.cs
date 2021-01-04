﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
public class Player_Controller : MonoBehaviour {
    Rigidbody2D Rigid;
    public float Movement_Speed = 10f;
    private float Movement = 0;
    private int Direction = 1;
    private Vector3 Player_LocalScale;
	private float move;
    public Sprite[] Spr_Player = new Sprite[2];
	public float speed;
	public float destinationX;
	public float destinationY;
	// Use this for initialization
	void Start () 
    {
        Rigid = GetComponent<Rigidbody2D>();
        Player_LocalScale = transform.localScale;

		// Rigid.velocity = 0;
	}
	
	// Update is called once per frame
	void Update () 
    {
		StreamReader sr = new StreamReader ("login.txt", Encoding.UTF8);
		string line;
		line = sr.ReadLine ().ToString ();
		string[] arr = line.Split (' ');
		int control = int.Parse(arr [0]);
		destinationX = float.Parse (arr [1]);
		destinationY = float.Parse (arr [2]);
        // Set Movement value
		if (control == 1)
			move = 0.5f;
		else if (control == -1)
			move = -0.5f;
		else
			move = 0;
		Movement =  move * Movement_Speed; //Input.GetAxis("Horizontal") * Movement_Speed; //Input.acceleration.x * Movement_Speed;
        
        // Player look right or left
        if (Movement > 0)
            transform.localScale = new Vector3(Player_LocalScale.x, Player_LocalScale.y, Player_LocalScale.z);
        else if (Movement < 0)
            transform.localScale = new Vector3(-Player_LocalScale.x, Player_LocalScale.y, Player_LocalScale.z);
	}

    void FixedUpdate()
    {
		// print (transform.position);
        // Calculate player velocity
        Vector2 Velocity = Rigid.velocity;
        Velocity.x = Movement;
        Rigid.velocity = Velocity;
		speed = Velocity.y;
        // Player change sprite
        if (Velocity.y < 0)
        {
            GetComponent<SpriteRenderer>().sprite = Spr_Player[0];

            // Active player collider
            GetComponent<BoxCollider2D>().enabled = true;

            // Fall propeller after fly up
            Propeller_Fall();
        }
        else
        {
            GetComponent<SpriteRenderer>().sprite = Spr_Player[1];

            // Deactive player collider
            GetComponent<BoxCollider2D>().enabled = false;
        }

        // Player wrap
        Vector3 Top_Left = Camera.main.ScreenToWorldPoint(new Vector3(0, 0, 0));
        float Offset = 0.5f;

        if (transform.position.x > -Top_Left.x + Offset)
            transform.position = new Vector3(Top_Left.x - Offset, transform.position.y, transform.position.z);
        else if(transform.position.x < Top_Left.x - Offset)
            transform.position = new Vector3(-Top_Left.x + Offset, transform.position.y, transform.position.z);
    }

    void Propeller_Fall()
    {
        if (transform.childCount > 0)
        {
            transform.GetChild(0).GetComponent<Animator>().SetBool("Active", false);
            transform.GetChild(0).GetComponent<Propeller>().Set_Fall(gameObject);
            transform.GetChild(0).parent = null;
        }
    }
	public float getSpeed(){
		return speed;
	}
}
