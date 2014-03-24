#include <string.h>
#include <iostream>
#include <stdlib.h>

int cntTotal = 0;
int BOARDSIZE=11;

bool markboard(bool* b, int row, int col){
	for(int i =row;i<BOARDSIZE;++i){
		*(b+i*BOARDSIZE+col) = true;
	}
	for (int i=row+1, j=col-1 ; i<BOARDSIZE && j>=0; ++i, --j)
		*(b+i*BOARDSIZE+j)=true;
	for(int i = row+1, j=col+1; i<BOARDSIZE && j<BOARDSIZE; ++i, ++j)
		*(b+i*BOARDSIZE+j)=true;

	return true;
}

bool IsQuerePos(bool* board, int idx){

	bool *b = new bool[BOARDSIZE*BOARDSIZE];
	for(int i = 0;i<BOARDSIZE; ++i){
		if(*(board+idx*BOARDSIZE+i) )
			continue;
		if(idx == BOARDSIZE-1){
			cntTotal ++;
			std::cout<<cntTotal<<"\r";
		}
		else{
			memcpy(b, board, sizeof(bool)* BOARDSIZE*BOARDSIZE);
		
			markboard(b, idx, i);
		  	IsQuerePos(b, idx+1);
		}
	}
	delete b;
}


int main(int argc, char** argv){
	if(argc ==2)
		BOARDSIZE = atoi(argv[1]);
	std::cout<< argc << std::endl;
	bool *board = new bool[BOARDSIZE*BOARDSIZE];
	bool *p = board;
	for(int i = 0; i<BOARDSIZE; i++){
		for(int j=0; j<BOARDSIZE;j++)
			*p++ = false;
	}
	IsQuerePos(board, 0);	
	std::cout<<cntTotal<<std::endl;
	delete board;
}


