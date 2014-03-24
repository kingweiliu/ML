#include <iostream>
#include <stdlib.h>

int cntTotal = 0;
int BOARDSIZE=11;

bool check(bool* b, int row, int col){
	for(int i =0;i<row;++i){
		if(*(b+i*BOARDSIZE+col))
			return false;		
	}
	for (int i=row-1, j=col-1 ; i>=0&& j>=0; --i, --j)
		if(*(b+i*BOARDSIZE+j)) return false;
	for(int i = row-1, j=col+1; i>=0 && j<BOARDSIZE; --i, ++j)
		if(*(b+i*BOARDSIZE+j)) return false;

	return true;
}

bool IsQuerePos(bool* b, int idx){
	for(int i = 0;i<BOARDSIZE; ++i){
		*(b+idx*BOARDSIZE+i) = true;
		
		if(check(b, idx, i)){
			if(idx == BOARDSIZE-1 ){
				cntTotal ++;
				std::cout<<cntTotal<<"\r";
				return true;
			}
			IsQuerePos(b, idx+1);
		}
		*(b+idx*BOARDSIZE+i) = false;	
	}
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


