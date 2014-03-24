#include <iostream>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int cntTotal = 0;
int board_size=11;

pthread_t* array_threads = NULL;
int count_threads = 0;

bool markboard(bool* b, int row, int col){
	for(int i =row;i<board_size;++i){
		*(b+i*board_size+col) = true;
	}
	for (int i=row+1, j=col-1 ; i<board_size && j>=0; ++i, --j)
		*(b+i*board_size+j)=true;
	for(int i = row+1, j=col+1; i<board_size && j<board_size; ++i, ++j)
		*(b+i*board_size+j)=true;

	return true;
}

bool IsQuerePos(bool* board, int idx){

	bool *b = new bool[board_size*board_size];
	for(int i = 0;i<board_size; ++i){
		if(*(board+idx*board_size+i) )
			continue;
		if(idx == board_size-1)
			cntTotal ++;
		else{
			memcpy(b, board, sizeof(bool)* board_size*board_size);
		
			markboard(b, idx, i);
	  	IsQuerePos(b, idx+1);
		}
	}
	delete b;
}

class Thread{
	public:
		Thread(){
			pthread_create(&thread_, NULL, ThreadFunc, this);	
		}

		static void* ThreadFunc(void* param){
			Thread* pThread = (Thread*)param;
			pThread->Run();
		}

		void Run(){
			std::cout<<thread_<<std::endl;
		}
		void finish(){
			pthread_join(thread_, NULL);
		}
	private:
		pthread_t thread_;

};


class TaskThreadMgr{
	public:
		TaskThreadMgr(int thread_count){
			std::cout<<"task thread mgr ctor"<<std::endl;
			thread_count_ = thread_count;
			pthreads_ = new Thread*[thread_count];
			for(int i = 0; i< thread_count_;++i){
				pthreads_[i] = new Thread();	
				std::cout<<i<<std::endl;
			}
		}

		void Run(){
			for(int i =0;i<thread_count_;++i){
				(*pthreads_)[i].finish();
				delete pthreads_[i];
			}
			delete[] pthreads_;
		}


	private:
		int thread_count_;
		Thread** pthreads_;
};

int main(int argc, char** argv){
	if(argc ==2)
		board_size = atoi(argv[1]);
	else if(argc==3){
		board_size = atoi(argv[1]);
		count_threads = atoi(argv[2]);
	}
	std::cout<< argc << std::endl;
	bool *board = new bool[board_size*board_size];
	bool *p = board;
	for(int i = 0; i<board_size; i++){
		for(int j=0; j<board_size;j++)
			*p++ = false;
	}
	TaskThreadMgr mgr(4);
	mgr.Run();
	/*
	pthread_t thread1;
	pthread_create(&thread1, NULL, thread_func, NULL);
	
	while(true)
		sleep(1);
	//IsQuerePos(board, 0);	
	*/
	std::cout<<cntTotal<<std::endl;
	delete board;
}


