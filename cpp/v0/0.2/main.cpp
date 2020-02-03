// main.cpp
// includes
#include<graphics.h>
#include<cmath>
#include<ctime>
#include<queue>
#include<iostream>
#include<algorithm>
#include<cstdio>
#include <Windows.h>
using namespace std;


// constants definition
const double G = 1; // gravitation constant
const bool gravity = true; // gravitation simulation availability
const int width = GetSystemMetrics(SM_CXSCREEN)-100, height = GetSystemMetrics(SM_CYSCREEN)-100;
const bool refresh = true;
// functions definition


template<typename T>
T rnd(T _min, T _max) // [_min, _max] random value generator
{
	T temp;
	if (_min > _max)
	{
		temp = _max;
		_max = _min;
		_min = temp;
	}
	return rand() / (double)RAND_MAX *(_max - _min) + _min;
}


int valuence(double x) {
	//return the valuence of x
	if(x>0)return 1;
	if(x<0) return -1;
	return 0; 
}


// body structure definition
struct body {
	double x, y; // position (x, y)
	double dx, dy; // velocity(horizontal & vertical)
	double m; // mass
	bool affected; // availability of being affected of non-contact forces
	body(double _x=0, double _y=0, double _dx=0, double _dy=0, double _m=0, bool _affected=true) {
		x = _x; y = _y; dx = _dx; dy = _dy; m = _m;
		affected = _affected;
	}
};

int n; // the biggest used index of array B
bool used[100]; // used[i] tells if B[i] is in use
queue<int> que; // when a body is deleted, its index will be pushed into que
body B[100];
//int tmpcnt;
//int tcur;

// body attributes functions

double R_m(double m) { // get radius by mass
	return 2.0 * sqrt(m);
}
double R(int i) { // get radius by index
	return R_m(B[i].m);
}


// bodies allocation functions

void release(int i) { // release space for reuse
	used[i] = false;
	B[i] = body();
	que.push(i);
}

int get_index() { // return an available index for a new body
	// a new body at the right index must be immediately created after calling this function
	if(!que.empty()){
		int res = que.front();
		used[res]=true;
		que.pop();
		B[res] = body();
		return res;
	}
	used[++n] = true;
	return n;
}


void jet(int i, double theta) { // jet out a new body from B[i], direction represented by angle
	
	double _m = B[i].m/40.0, _c = cos(theta), _s = sin(theta);
	double _x = B[i].x+_c*(R(i)+2*R_m(_m)), _y=B[i].y+_s*(R(i)+2*R_m(_m)), _dx=_c*10, _dy=_s*10;
	int j = get_index();
	//tcur = j;
	B[j] = body(_x,_y,_dx,_dy,_m);
	B[i].m -= B[j].m;
	B[i].dx += -B[j].m*B[j].dx/B[i].m;
	B[i].dy += -B[j].m*B[j].dy/B[i].m;
	//tmpcnt++;
}

void jet(int i, double vx, double vy) { // jet out a new body from B[i], direction represented by vector
    jet(i, atan2(vy, vx)); // just calculate angle by vector and do the same
}


// main
int main()
{
	initgraph(width, height, INIT_RENDERMANUAL);
	srand((unsigned)time(NULL));
	n = -1; //tcur = -1;
	int cd = 50; // avoid over-clicking
	for(int i=0; i<=10;++i) {
		int j = get_index();
		B[j] = body(rnd(0,width), rnd(0,height), rnd(-5,5), rnd(-5,5), rnd(20, 100));
		if(i==0) B[j].m = 500;
	}
	setcolor(EGERGB(0x00,0x00,0x00)); setfillcolor(EGERGB(0x00,0x00,0x00));
	for(;is_run();delay_fps(25)) {
		if(cd <=0)
		{
			jet(0,-10, -10); cd = 50;
		}
		else cd--;
		if(refresh) cleardevice();
		//xyprintf(0,0,"Chaos Emulator; tmpcnt: %d", tmpcnt);
		//xyprintf(200, 0, "B[0]:x:%.3f;y:%.3f;dx:%.3f;dy:%.3f;m:%.3f",B[0].x,B[0].y,B[0].dx,B[0].dy,B[0].m);
		setbkcolor(EGERGB(0xff,0xff,0xff));
		
		 //test
		int _s = 0;
		for(int i=0;i<=n;++i) {
			if(used[i] && B[i].m==0) release(i);
			if(!used[i]) continue;
			if(i==0) setfillcolor(EGERGB(0xff,0x00,0x00));
			//else if (i==tcur) setfillcolor(EGERGB(0x00, 0xff,0xff));
			++_s;
			fillellipse(B[i].x, B[i].y, R(i),R(i));
			setfillcolor(EGERGB(0x00,0x00,0x00));
		}
		//setfillcolor(EGERGB(0x00,0xff,0xff));
	    //fillellipse(B[0].x+cos(M_PI)*R(0),B[0].y+sin(M_PI)*R(0),3,3);
	    //setfillcolor(EGERGB(0x00,0x00,0x00));
		//if(tcur!=-1)line(B[0].x,B[0].y,B[tcur].x,B[tcur].y);
		//xyprintf(0,50,"Bodies: %d; n: %d; que.size(): %d", _s, n, que.size());
		// absorbing
		for(int i=0;i<=n;++i) { // enumerate the pairs of bodies
			if(!used[i]) continue;
			for(int j=i+1;j<=n;++j) {
				if(!used[j]) continue;
				double disq = (B[i].x-B[j].x)*(B[i].x-B[j].x)+(B[i].y-B[j].y)*(B[i].y-B[j].y);
				if((R(i)+R(j))*(R(i)+R(j))>disq) // one should be absorbed by the other
				{
					double subq = (B[i].dx-B[j].dx)*(B[i].dx-B[j].dx)+(B[i].dy-B[j].dy)*(B[i].dy-B[j].dy); // the mass should be transmitted
					if(B[i].m>B[j].m)
					{
						if(R(i)*R(i)>disq || subq>B[j].m) subq = B[j].m; // j is inside i
						B[i].m += subq;
						B[i].dx = (B[j].dx*subq+B[i].dx*B[i].m)/(B[i].m+subq);
						B[i].dy = (B[j].dy*subq+B[i].dy*B[i].m)/(B[i].m+subq);
						B[j].m -= subq;
					}
					else {
						if(R(j)*R(j)>disq) subq = B[i].m; // i is inside j
						B[j].m += min(B[i].m,subq);
						B[j].dx = (B[i].dx*subq+B[j].dx*B[j].m)/(B[j].m+subq);
						B[j].dy = (B[i].dy*subq+B[j].dy*B[j].m)/(B[j].m+subq);
						B[i].m -= min(B[i].m,subq);
					}
				}
			}
		}
		
		// calculate the gravitation between every two bodies i & j, and apply the acceleration
		for(int i=0; gravity && i<=n;++i)
		{
			if(!used[i]) continue;
			for(int j=i+1;j<=n;++j)
			{
				if(!used[j]) continue;
				if(B[i].m==0||B[j].m==0) continue;
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
		}
		// update positions
		for(int i=0;i<=n;++i)
		{
			if(!used[i]) continue;
			B[i].x+=B[i].dx;
			B[i].y+=B[i].dy;
			if(B[i].x+R(i)>=width) B[i].dx=-abs(B[i].dx);
			if(B[i].x-R(i)<=0) B[i].dx=abs(B[i].dx);
			if(B[i].y+R(i)>=height) B[i].dy=-abs(B[i].dy);
			if(B[i].y-R(i)<=0) B[i].dy=abs(B[i].dy);
		}
	}
	closegraph();
	return 0;
	
}
