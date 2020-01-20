#include<graphics.h>
#include<cmath>
const int width = 1500, height = 1000;
const double G = 10;
const bool refresh = true;
int n = 3; // the amount of bodies
int valuence(double x) {
	//return the valuence of x
	if(x>0)return 1;
	if(x<0) return -1;
	return 0; 
}
class body {
	public:
		double x, y; // position (x, y)
		double dx, dy; // velocity(horizontal & vertical)
		double m; // mass
		bool affected; // if this body is under influence of gravitation
		color_t color;
	body()
	{
		this->x = this->y = this->dx = this->dy = this->m = this->affected = 0; this->color = EGERGB(0xff,0xff,0xff);
	}
	body(double x, double y, double dx, double dy, double m, bool affected, color_t color)
	{
		this->x = x;
		this->y = y;
		this->dx = dx;
		this->dy = dy;
		this->m = m;
		this->affected = affected;
		this->color = color;
	}
};
body B[4];
int main()
{
	initgraph(width, height, INIT_RENDERMANUAL);
	B[0] = body(width/2, height/2, 0, 0, 300, false, EGERGB(0xff,0x00,0x00)); // body a
	B[1] = body(width/2, height*2.5/3-30, 1.5, 0, 40, true,EGERGB(0xff,0x00,0xff)); // body b
	B[2] = body(width/2, height*2.5/3+30, 4.5, 0, 40, true, EGERGB(0xff,0xff,0x00)); // body c
	//B[0] = body(width/2-30, height/2-30, 0, -4, 40, true, EGERGB(0xff,0x00,0x00));
	//B[1] = body(width/2+30, height/2-30, 4, 0, 40, true, EGERGB(0x00,0xff,0x00));
	//B[2] = body(width/2+30, height/2+30, 0, 4, 40, true, EGERGB(0xff,0xff,0x00));
	//B[3] = body(width/2-30, height/2+30, -4, 0, 40, true, EGERGB(0x00,0x00,0xff));
	for(;is_run();delay_fps(25)) {
		if(refresh) cleardevice();
		setbkcolor(EGERGB(0x00,0x00,0x00));
		//render the bodies
		for(int i=0;i<n;++i) {
			setfillcolor(B[i].color);
			setcolor(B[i].color);
			fillellipse(B[i].x, B[i].y, 2*sqrt(B[i].m),2*sqrt(B[i].m));
		}
		/*
		setcolor(B[0].color);
		setfillcolor(B[0].color);
		fillellipse((B[1].x+B[2].x)/2, (B[1].y+B[2].y)/2, 2, 2);*/
		// calculate the gravitation between every two bodies i & j, and apply the acceleration
		for(int i=0;i<n;++i)
			for(int j=i+1;j<n;++j)
			{
				if(!(B[i].affected||B[j].affected)) continue;
				double xl = abs(B[i].x-B[j].x), yl = abs(B[i].y-B[j].y); // horizontal & vertical distance
				double l = sqrt(xl*xl+yl*yl); // distance
				double F = G*B[i].m*B[j].m/(l*l); // the gravitational force
				double xF = F*xl/l, yF = F*yl/l; // split the force into horizontal & vertical forces to calculate & represent conveniently
				if(B[i].affected)
				{
					B[i].dx += valuence(B[j].x-B[i].x)*xF/B[i].m;
					B[i].dy += valuence(B[j].y-B[i].y)*yF/B[i].m;
				}
				if(B[j].affected)
				{
					B[j].dx += valuence(B[i].x-B[j].x)*xF/B[j].m;
					B[j].dy += valuence(B[i].y-B[j].y)*yF/B[j].m;
				}
			}
		// update positions
		for(int i=0;i<n;++i)
		{
			B[i].x+=B[i].dx;
			B[i].y+=B[i].dy;
		}
	}
	closegraph();
	return 0;
	
}
