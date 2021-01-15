module Tetris(output reg [7:0]R,output reg [3:0]COMM,output reg beep,input up,down,left,right,sdown,CLK, output reg[3:0] Light);
	divfreq C0(CLK,CLK_div,CLK_Hz10);
	reg [9:0] down_count;
	reg [2:0] SHOW_COUNT;
	reg [11:0] SHOW_Map [7:0];
	reg [11:0] Map [7:0];
	reg [0:3] BLOCK [0:3];
	reg [3:0] ran;
	reg [3:0] state;
	reg OVER,PLAY,Start;
	reg HIT_FLOOR = 0;
	int x=5,y=11;
	initial
		begin
			beep = 0;
			OVER = 0;
			PLAY = 1;
			Start = 0;

			//遊戲開始時，會產生一個 T 圖案
							 //11109876543210Y	  X
			SHOW_Map = '{12'b111111111111,	//7
							 12'b111100111111,	//6
					  	 	 12'b111100111111,	//5
					  	 	 12'b111100000001,	//4
					  	 	 12'b111100000001,	//3
					  	 	 12'b111100111111,	//2
					  	 	 12'b111100111111,	//1
					  	 	 12'b111111111111};	//0
							 //11109876543210Y     X

				Map	= '{12'b111111111111,	//7
							 12'b111111111111,	//6
					  	 	 12'b111111111111,	//5
					  	 	 12'b111111111111,	//4
					  	 	 12'b111111111111,	//3
					  	 	 12'b111111111111,	//2
					  	 	 12'b111111111111,	//1
					  	 	 12'b111111111111}; 	//0
		end
	
	always@ (posedge up)
	begin
		Start = 1;
	end
	
	always@(posedge CLK_Hz10) //產生一個新方塊
	begin
	if(Start) begin
		reg JUDGE;					
		if(beep && down_count==3)
			beep = 0; 
		if((PLAY==1 || OVER==1) && (up||down||left||right)&&(down_count%6==0))begin //	start over beep
		down_count = 0;
		beep = 1;
		Light <= 4'b0000;
		Map='{12'b111111111111,	//7
			   12'b111111111111,	//6
			   12'b111111111111,	//5
			   12'b111111111111,	//4
			   12'b111111111111,	//3
			   12'b111111111111,	//2
			   12'b111111111111,	//1
			   12'b111111111111};//0
		PLAY = 0;
		OVER = 0;
						case(ran) //產生方塊，並給定方塊樣式
									  //0123y   x
					0:begin
						BLOCK = '{4'b1111, //0
									 4'b1100, //1
									 4'b1100, //2
									 4'b1111};//3
						state = 0;
					end			 
					1: begin
						BLOCK = '{4'b1110,
									 4'b1110,
									 4'b1110,
									 4'b1110};
						state = 1;
					end			 
					2: begin
						BLOCK = '{4'b1111,
									 4'b0000,
									 4'b1111,
									 4'b1111};
						state = 2;
					end			 									 
					3: begin
						BLOCK = '{4'b1110,
									 4'b1100,
									 4'b1101,
									 4'b1111};
						state = 3;
					end
					4: begin
						BLOCK = '{4'b1111,
									 4'b1001,
									 4'b1100,
									 4'b1111};
						state = 4;
					end									 
					5: begin
						BLOCK = '{4'b1111,
									 4'b1110,
									 4'b1000,
									 4'b1111};
						state = 5;
					end									 
					6: begin
						BLOCK = '{4'b1101,
									 4'b1101,
									 4'b1100,
									 4'b1111};
						state = 6;
					end									 
					7: begin
						BLOCK = '{4'b1111,
									 4'b1000,
									 4'b1011,
									 4'b1111};
						state = 7;
					end									 
					8: begin
						BLOCK = '{4'b1111,
									 4'b1100,
									 4'b1110,
									 4'b1110};
						state = 8;
					end									 
					9: begin
						BLOCK = '{4'b1110,
									 4'b1100,
									 4'b1110,
									 4'b1111};
						state = 9;
					end									 
					10:begin
						BLOCK = '{4'b1111,
									 4'b1101,
									 4'b1000,
									 4'b1111};
						state = 10;
					end									 
					11:begin
						BLOCK = '{4'b1101,
									 4'b1100,
									 4'b1101,
									 4'b1111};
						state = 11;
					end									 
					12:begin
						BLOCK = '{4'b1111,
									 4'b1000,
									 4'b1101,
									 4'b1111};
						state = 12;
					end									  
				endcase
	end
		
		if(left==1) begin
				JUDGE = 1;			//判斷方塊向左移時，是否會與現有方塊重疊
				if(!(BLOCK[0][0]|Map[x-1][y])||!(BLOCK[0][1]|Map[x-1][y-1])||!(BLOCK[0][2]|Map[x-1][y-2])||!(BLOCK[0][3]|Map[x-1][y-3])
				||!(BLOCK[1][0]|Map[x-2][y])||!(BLOCK[1][1]|Map[x-2][y-1])||!(BLOCK[1][2]|Map[x-2][y-2])||!(BLOCK[1][3]|Map[x-2][y-3])
				||!(BLOCK[2][0]|Map[x-3][y])||!(BLOCK[2][1]|Map[x-3][y-1])||!(BLOCK[2][2]|Map[x-3][y-2])||!(BLOCK[2][3]|Map[x-3][y-3])
				||!(BLOCK[3][0]|Map[x-4][y])||!(BLOCK[3][1]|Map[x-4][y-1])||!(BLOCK[3][2]|Map[x-4][y-2])||!(BLOCK[3][3]|Map[x-4][y-3]))
					JUDGE = 0;
					
				if(JUDGE && ((x>1&&state==2) || (x>2&&state!=1) || x>3))	//判斷方塊移動時，是否會撞到邊界
					x = x - 1;						//向左移
		end
		
		if(right==1) begin
				JUDGE = 1;	//判斷方塊向右移時，是否會與現有方塊重疊					//if go right no hit
				if(!(BLOCK[0][0]|Map[x+1][y])||!(BLOCK[0][1]|Map[x+1][y-1])||!(BLOCK[0][2]|Map[x+1][y-2])||!(BLOCK[0][3]|Map[x+1][y-3])
				||!(BLOCK[1][0]|Map[x][y])||!(BLOCK[1][1]|Map[x][y-1])||!(BLOCK[1][2]|Map[x][y-2])||!(BLOCK[1][3]|Map[x][y-3])
				||!(BLOCK[2][0]|Map[x-1][y])||!(BLOCK[2][1]|Map[x-1][y-1])||!(BLOCK[2][2]|Map[x-1][y-2])||!(BLOCK[2][3]|Map[x-1][y-3])
				||!(BLOCK[3][0]|Map[x-2][y])||!(BLOCK[3][1]|Map[x-2][y-1])||!(BLOCK[3][2]|Map[x-2][y-2])||!(BLOCK[3][3]|Map[x-2][y-3]))
					JUDGE = 0;
					
				if(JUDGE && (x<7||(x<8&&state!=1&&state!=3&&state!=6&&state!=9&&state!=11)))	//判斷方塊移動時，是否會撞到邊界
					x = x + 1;								//向右移
		end
		
		if(up==1)begin			// 變換方向
			reg [0:3] BLOCK2[0:3];
				case(state)
					0:begin
						BLOCK2 = '{4'b1111,
									  4'b1100,
									  4'b1100,
									  4'b1111};
					end
					2:begin
						BLOCK2 ='{4'b1110,
									 4'b1110,
									 4'b1110,
									 4'b1110};
					end			 
					1: begin
						BLOCK2 = '{4'b1111,
									 4'b0000,
									 4'b1111,
									 4'b1111};
					end			 									 
					4: begin
						BLOCK2 = '{4'b1110,
									 4'b1100,
									 4'b1101,
									 4'b1111};
					end
					3: begin
						BLOCK2 = '{4'b1111,
									 4'b1001,
									 4'b1100,
									 4'b1111};
					end									 
					8: begin
						BLOCK2 = '{4'b1111,
									 4'b1110,
									 4'b1000,
									 4'b1111};
					end									 
					5: begin
						BLOCK2 = '{4'b1101,
									 4'b1101,
									 4'b1100,
									 4'b1111};
					end									 
					6: begin
						BLOCK2 = '{4'b1111,
									 4'b1000,
									 4'b1011,
									 4'b1111};
					end									 
					7: begin
						BLOCK2 = '{4'b1111,
									 4'b1100,
									 4'b1110,
									 4'b1110};
					end									 
					12: begin
						BLOCK2 = '{4'b1110,
									 4'b1100,
									 4'b1110,
									 4'b1111};
					end									 
					9:begin
						BLOCK2 = '{4'b1111,
									  4'b1101,
									  4'b1000,
									  4'b1111};
					end									 
					10:begin
						BLOCK2 = '{4'b1101,
									  4'b1100,
									  4'b1101,
									  4'b1111};
					end									 
					11:begin
						BLOCK2 = '{4'b1111,
									  4'b1000,
									  4'b1101,
									  4'b1111};
					end									  
				endcase
				JUDGE = 1;     			//判斷方塊旋轉時，是否會與現有方塊重疊			
				if(!(BLOCK2[0][0]|Map[x][y])||!(BLOCK2[0][1]|Map[x][y-1])||!(BLOCK2[0][2]|Map[x][y-2])||!(BLOCK2[0][3]|Map[x][y-3])
				||!(BLOCK2[1][0]|Map[x-1][y])||!(BLOCK2[1][1]|Map[x-1][y-1])||!(BLOCK2[1][2]|Map[x-1][y-2])||!(BLOCK2[1][3]|Map[x-1][y-3])
				||!(BLOCK2[2][0]|Map[x-2][y])||!(BLOCK2[2][1]|Map[x-2][y-1])||!(BLOCK2[2][2]|Map[x-2][y-2])||!(BLOCK2[2][3]|Map[x-2][y-3])
				||!(BLOCK2[3][0]|Map[x-3][y])||!(BLOCK2[3][1]|Map[x-3][y-1])||!(BLOCK2[3][2]|Map[x-3][y-2])||!(BLOCK2[3][3]|Map[x-3][y-3]))
					JUDGE = 0;
				if(JUDGE) begin
					BLOCK = BLOCK2;
					case(state)  //change block			//旋轉
						1:state=2;
						2:state=1;
						3:state=4;
						4:state=3;
						5:state=6;
						6:state=7;
						7:state=8;
						8:state=5;
						9:state=10;
						10:state=11;
						11:state=12;
						12:state=9;
					endcase
				end
		end
		
		
		if(down_count > 9)	//判斷掉落次數
			down_count = 0;
		else
			down_count = down_count + 1'b1;
			
		if(sdown==1&&down_count%3==0)begin //快速下降
			for(int i=3;i<8;i++) begin
				JUDGE = 1;					//判斷方塊快速下降時，是否會與現有方塊重疊					
				if(!(BLOCK[0][0]|Map[x][i])||!(BLOCK[0][1]|Map[x][i-1])||!(BLOCK[0][2]|Map[x][i-2])||!(BLOCK[0][3]|Map[x][i-3])
				||!(BLOCK[1][0]|Map[x-1][i])||!(BLOCK[1][1]|Map[x-1][i-1])||!(BLOCK[1][2]|Map[x-1][i-2])||!(BLOCK[1][3]|Map[x-1][i-3])
				||!(BLOCK[2][0]|Map[x-2][i])||!(BLOCK[2][1]|Map[x-2][i-1])||!(BLOCK[2][2]|Map[x-2][i-2])||!(BLOCK[2][3]|Map[x-2][i-3])
				||!(BLOCK[3][0]|Map[x-3][i])||!(BLOCK[3][1]|Map[x-3][i-1])||!(BLOCK[3][2]|Map[x-3][i-2])||!(BLOCK[3][3]|Map[x-3][i-3]))
					JUDGE = 0;
				else begin
					if(i<y)//if hit stop at y
						y = i;				//直接下降至碰到現有已堆疊的方塊或最底部
				end
			end

			SHOW_Map = Map;
			for(int i=0;i<4;i++) begin				//顯示新方塊
				for(int j=0;j<4;j++) begin
					if(!BLOCK[i][j])
						SHOW_Map[x-i][y-j] = 0;
				end
			end
			Map = SHOW_Map;
		end
		if(down_count==10 || down || sdown) begin		//判斷方塊下降時，是否會與現有方塊重疊	
				JUDGE = 1;
				if(!(BLOCK[0][0]|Map[x][y-1])||!(BLOCK[0][1]|Map[x][y-2])||!(BLOCK[0][2]|Map[x][y-3])||!(BLOCK[0][3]|Map[x][y-4])
				||!(BLOCK[1][0]|Map[x-1][y-1])||!(BLOCK[1][1]|Map[x-1][y-2])||!(BLOCK[1][2]|Map[x-1][y-3])||!(BLOCK[1][3]|Map[x-1][y-4])
				||!(BLOCK[2][0]|Map[x-2][y-1])||!(BLOCK[2][1]|Map[x-2][y-2])||!(BLOCK[2][2]|Map[x-2][y-3])||!(BLOCK[2][3]|Map[x-2][y-4])
				||!(BLOCK[3][0]|Map[x-3][y-1])||!(BLOCK[3][1]|Map[x-3][y-2])||!(BLOCK[3][2]|Map[x-3][y-3])||!(BLOCK[3][3]|Map[x-3][y-4]))
					JUDGE = 0;
	
			if(JUDGE == 1 && y>3) begin
				if(!sdown)			 		
					y = y-1;		//下降		
			end
			else begin
				down_count = 0;
				Map = SHOW_Map;
				if(!(Map[0][8]&Map[1][8]&Map[2][8]&Map[3][8]&Map[4][8]&Map[5][8]&Map[6][8]&Map[7][8])) //堆疊方塊碰到最頂端，則遊戲結束
					OVER = 1;
				else begin
				case(ran%13)     //random block
									  //0123y	x
					0:begin
						BLOCK = '{4'b1111, //0
									 4'b1100, //1
									 4'b1100, //2
									 4'b1111};//3
						state = 0;
					end			 
					1: begin
						BLOCK = '{4'b1110,
									 4'b1110,
									 4'b1110,
									 4'b1110};
						state = 1;
					end			 
					2: begin
						BLOCK = '{4'b1111,
									 4'b0000,
									 4'b1111,
									 4'b1111};
						state = 2;
					end			 									 
					3: begin
						BLOCK = '{4'b1110,
									 4'b1100,
									 4'b1101,
									 4'b1111};
						state = 3;
					end
					4: begin
						BLOCK = '{4'b1111,
									 4'b1001,
									 4'b1100,
									 4'b1111};
						state = 4;
					end									 
					5: begin
						BLOCK = '{4'b1111,
									 4'b1110,
									 4'b1000,
									 4'b1111};
						state = 5;
					end									 
					6: begin
						BLOCK = '{4'b1101,
									 4'b1101,
									 4'b1100,
									 4'b1111};
						state = 6;
					end									 
					7: begin
						BLOCK = '{4'b1111,
									 4'b1000,
									 4'b1011,
									 4'b1111};
						state = 7;
					end									 
					8: begin
						BLOCK = '{4'b1111,
									 4'b1100,
									 4'b1110,
									 4'b1110};
						state = 8;
					end									 
					9: begin
						BLOCK = '{4'b1110,
									 4'b1100,
									 4'b1110,
									 4'b1111};
						state = 9;
					end									 
					10:begin
						BLOCK = '{4'b1111,
									  4'b1101,
									  4'b1000,
									  4'b1111};
						state = 10;
					end									 
					11:begin
						BLOCK = '{ 4'b1101,
									  4'b1100,
									  4'b1101,
									  4'b1111};
						state = 11;
					end									 
					12:begin
						BLOCK = '{4'b1111,
									  4'b1000,
									  4'b1101,
									  4'b1111};
						state = 12;
					end									  
				endcase
					x = 5;
					y = 11;                                                                                
								
				//消掉一橫排，方塊向下遞補 及 分數增加	
				if(Map[0][7]==0&&Map[1][7]==0&&Map[2][7]==0&&Map[3][7]==0&&Map[4][7]==0&&Map[5][7]==0&&Map[6][7]==0&&Map[7][7]==0) begin
					Map[0][11:7] = $signed(Map[0][11:7]) >>> 1;
					Map[1][11:7] = $signed(Map[1][11:7]) >>> 1;
					Map[2][11:7] = $signed(Map[2][11:7]) >>> 1;
					Map[3][11:7] = $signed(Map[3][11:7]) >>> 1;
					Map[4][11:7] = $signed(Map[4][11:7]) >>> 1;
					Map[5][11:7] = $signed(Map[5][11:7]) >>> 1;
					Map[6][11:7] = $signed(Map[6][11:7]) >>> 1;
					Map[7][11:7] = $signed(Map[7][11:7]) >>> 1;
					beep = 1;
					Light <= Light +1'b1;
				end
				if(Map[0][6]==0&&Map[1][6]==0&&Map[2][6]==0&&Map[3][6]==0&&Map[4][6]==0&&Map[5][6]==0&&Map[6][6]==0&&Map[7][6]==0) begin
					Map[0][11:6] = $signed(Map[0][11:6]) >>> 1;
					Map[1][11:6] = $signed(Map[1][11:6]) >>> 1;
					Map[2][11:6] = $signed(Map[2][11:6]) >>> 1;
					Map[3][11:6] = $signed(Map[3][11:6]) >>> 1;
					Map[4][11:6] = $signed(Map[4][11:6]) >>> 1;
					Map[5][11:6] = $signed(Map[5][11:6]) >>> 1;
					Map[6][11:6] = $signed(Map[6][11:6]) >>> 1;
					Map[7][11:6] = $signed(Map[7][11:6]) >>> 1;
					beep = 1;
					Light <= Light +1'b1;
				end
				if(Map[0][5]==0&&Map[1][5]==0&&Map[2][5]==0&&Map[3][5]==0&&Map[4][5]==0&&Map[5][5]==0&&Map[6][5]==0&&Map[7][5]==0) begin
					Map[0][11:5] = $signed(Map[0][11:5]) >>> 1;
					Map[1][11:5] = $signed(Map[1][11:5]) >>> 1;
					Map[2][11:5] = $signed(Map[2][11:5]) >>> 1;
					Map[3][11:5] = $signed(Map[3][11:5]) >>> 1;
					Map[4][11:5] = $signed(Map[4][11:5]) >>> 1;
					Map[5][11:5] = $signed(Map[5][11:5]) >>> 1;
					Map[6][11:5] = $signed(Map[6][11:5]) >>> 1;
					Map[7][11:5] = $signed(Map[7][11:5]) >>> 1;
					beep = 1;
					Light <= Light +1'b1;
				end
				if(Map[0][4]==0&&Map[1][4]==0&&Map[2][4]==0&&Map[3][4]==0&&Map[4][4]==0&&Map[5][4]==0&&Map[6][4]==0&&Map[7][4]==0) begin
					Map[0][11:4] = $signed(Map[0][11:4]) >>> 1;
					Map[1][11:4] = $signed(Map[1][11:4]) >>> 1;
					Map[2][11:4] = $signed(Map[2][11:4]) >>> 1;
					Map[3][11:4] = $signed(Map[3][11:4]) >>> 1;
					Map[4][11:4] = $signed(Map[4][11:4]) >>> 1;
					Map[5][11:4] = $signed(Map[5][11:4]) >>> 1;
					Map[6][11:4] = $signed(Map[6][11:4]) >>> 1;
					Map[7][11:4] = $signed(Map[7][11:4]) >>> 1;
					beep = 1;
					Light <= Light +1'b1;
				end
				if(Map[0][3]==0&&Map[1][3]==0&&Map[2][3]==0&&Map[3][3]==0&&Map[4][3]==0&&Map[5][3]==0&&Map[6][3]==0&&Map[7][3]==0) begin
					Map[0][11:3] = $signed(Map[0][11:3]) >>> 1;
					Map[1][11:3] = $signed(Map[1][11:3]) >>> 1;
					Map[2][11:3] = $signed(Map[2][11:3]) >>> 1;
					Map[3][11:3] = $signed(Map[3][11:3]) >>> 1;
					Map[4][11:3] = $signed(Map[4][11:3]) >>> 1;
					Map[5][11:3] = $signed(Map[5][11:3]) >>> 1;
					Map[6][11:3] = $signed(Map[6][11:3]) >>> 1;
					Map[7][11:3] = $signed(Map[7][11:3]) >>> 1;
					beep = 1;
					Light <= Light +1'b1;
				end
				if(Map[0][2]==0&&Map[1][2]==0&&Map[2][2]==0&&Map[3][2]==0&&Map[4][2]==0&&Map[5][2]==0&&Map[6][2]==0&&Map[7][2]==0) begin
					Map[0][11:2] = $signed(Map[0][11:2]) >>> 1;
					Map[1][11:2] = $signed(Map[1][11:2]) >>> 1;
					Map[2][11:2] = $signed(Map[2][11:2]) >>> 1;
					Map[3][11:2] = $signed(Map[3][11:2]) >>> 1;
					Map[4][11:2] = $signed(Map[4][11:2]) >>> 1;
					Map[5][11:2] = $signed(Map[5][11:2]) >>> 1;
					Map[6][11:2] = $signed(Map[6][11:2]) >>> 1;
					Map[7][11:2] = $signed(Map[7][11:2]) >>> 1;
					beep = 1;
					Light <= Light +1'b1;
				end
				if(Map[0][1]==0&&Map[1][1]==0&&Map[2][1]==0&&Map[3][1]==0&&Map[4][1]==0&&Map[5][1]==0&&Map[6][1]==0&&Map[7][1]==0) begin
					Map[0][11:1] = $signed(Map[0][11:1]) >>> 1;
					Map[1][11:1] = $signed(Map[1][11:1]) >>> 1;
					Map[2][11:1] = $signed(Map[2][11:1]) >>> 1;
					Map[3][11:1] = $signed(Map[3][11:1]) >>> 1;
					Map[4][11:1] = $signed(Map[4][11:1]) >>> 1;
					Map[5][11:1] = $signed(Map[5][11:1]) >>> 1;
					Map[6][11:1] = $signed(Map[6][11:1]) >>> 1;
					Map[7][11:1] = $signed(Map[7][11:1]) >>> 1;
					beep = 1;
					Light <= Light +1'b1;
				end
				if(Map[0][0]==0&&Map[1][0]==0&&Map[2][0]==0&&Map[3][0]==0&&Map[4][0]==0&&Map[5][0]==0&&Map[6][0]==0&&Map[7][0]==0) begin
					Map[0][11:0] = $signed(Map[0][11:0]) >>> 1;
					Map[1][11:0] = $signed(Map[1][11:0]) >>> 1;
					Map[2][11:0] = $signed(Map[2][11:0]) >>> 1;
					Map[3][11:0] = $signed(Map[3][11:0]) >>> 1;
					Map[4][11:0] = $signed(Map[4][11:0]) >>> 1;
					Map[5][11:0] = $signed(Map[5][11:0]) >>> 1;
					Map[6][11:0] = $signed(Map[6][11:0]) >>> 1;
					Map[7][11:0] = $signed(Map[7][11:0]) >>> 1;
					beep = 1;
					Light <= Light +1'b1;
				end
				end
			end
		end
		

		if(OVER) begin		//遊戲結束時，會顯示 X 圖案
							//11109876543210Y	  X
			SHOW_Map = '{12'b111111111111,	//7
							 12'b111110111101,	//6
					  	 	 12'b111111011011,	//5
					  	 	 12'b111111100111,	//4
					  	 	 12'b111111100111,	//3
					  	 	 12'b111111011011,	//2
					  	 	 12'b111110111101,	//1
					  	 	 12'b111111111111};	//0
		end
		else begin		//顯示現有成果於 8 x 8 LED 面板上										
			SHOW_Map = Map;
			SHOW_Map [x][y] 	  = Map [x][y] & BLOCK[0][0];
			SHOW_Map [x][y-1]   = Map [x][y-1] & BLOCK[0][1];
			SHOW_Map [x][y-2]   = Map [x][y-2] & BLOCK[0][2];
			SHOW_Map [x][y-3]   = Map [x][y-3] & BLOCK[0][3];
			SHOW_Map [x-1][y]   = Map [x-1][y] & BLOCK[1][0];
			SHOW_Map [x-1][y-1] = Map [x-1][y-1] & BLOCK[1][1];
			SHOW_Map [x-1][y-2] = Map [x-1][y-2] & BLOCK[1][2];
			SHOW_Map [x-1][y-3] = Map [x-1][y-3] & BLOCK[1][3];
			SHOW_Map [x-2][y]   = Map [x-2][y] & BLOCK[2][0];
			SHOW_Map [x-2][y-1] = Map [x-2][y-1] & BLOCK[2][1];
			SHOW_Map [x-2][y-2] = Map [x-2][y-2] & BLOCK[2][2];
			SHOW_Map [x-2][y-3] = Map [x-2][y-3] & BLOCK[2][3];
			SHOW_Map [x-3][y]	  = Map [x-3][y] & BLOCK[3][0];
			SHOW_Map [x-3][y-1] = Map [x-3][y-1] & BLOCK[3][1];
			SHOW_Map [x-3][y-2] = Map [x-3][y-2] & BLOCK[3][2];
			SHOW_Map [x-3][y-3] = Map [x-3][y-3] & BLOCK[3][3];
		end
	end
	end
		
	
	always@(posedge CLK_div)	// LED 面版相關設定
		begin
			ran <= ran + SHOW_COUNT;
			SHOW_COUNT <= SHOW_COUNT + 1'b1;
			COMM <= {SHOW_COUNT, 1'b1};
			R <= SHOW_Map[SHOW_COUNT][7:0];
		end
	
endmodule

module divfreq(input CLK,output reg CLK_div,output reg CLK_Hz10);	//時脈
	reg[30:0] Hz10_Count;
	reg[19:0] CLK_Count;
	always@(posedge CLK)
		begin
			if(CLK_Count >10000)
				begin 
					CLK_Count <= 0;
					CLK_div <= ~CLK_div;
				end
			else 
				CLK_Count <= CLK_Count + 1'b1;

			if(Hz10_Count > 2499999)
				begin
					CLK_Hz10 <= ~CLK_Hz10;
					Hz10_Count <= 0;
				end
			else
				Hz10_Count <= Hz10_Count + 1'b1;
				
		end
endmodule
