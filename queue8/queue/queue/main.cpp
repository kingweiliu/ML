#include <string.h>
#include <iostream>
#include <stdlib.h>
#include <windows.h>
#include <process.h>
#include "Job.h"
#include <time.h>
#include <string>
#include <WinNT.h>

class PerformanceHelper{
public:
  PerformanceHelper(const std::string& tag=""):m_tag(tag){
    tmStart = time(NULL);
    std::cout<<m_tag<<"start---"<<ctime(&tmStart)<<std::endl;
  }

  ~PerformanceHelper(){
    time_t tmEnd= time(NULL);
    std::cout<<m_tag<<"end---"<<ctime(&tmEnd)<<std::endl;
    double diff = difftime(tmEnd, tmStart);
    std::cout<<m_tag<<"duration:"<<diff<<std::endl;
  }
private:
  time_t tmStart;
  std::string m_tag;
};

class QueueEightDelegate{
public:

  void static Init(){
  }

  void static OnCalcComplete(long n){
    ::InterlockedExchangeAdd(&m_cnt, n);    
   // std::cout<<m_cnt<<"\r";
  }

  int static getCnt(){
    return m_cnt;
  }

private:
  static long m_cnt;
};

long QueueEightDelegate::m_cnt = 0;

class QueueEight{
public:
    QueueEight():m_board(NULL), m_board_size(8){ }

    QueueEight(int size):m_board_size(size){
        m_board = new bool[m_board_size*m_board_size];
        for( int i =0;i<m_board_size; ++i){
            for(int j=0; j<m_board_size; ++j){
                m_board[i*m_board_size + j] = false;
            }
        }
    }

    QueueEight(const QueueEight* qe){
        m_board_size = qe->m_board_size;
        m_board = new bool[m_board_size*m_board_size];
        memcpy(m_board, qe->m_board, sizeof(bool)* m_board_size*m_board_size);
    }

  ~QueueEight(){
    delete[] m_board;
  }

    void test(){
        std::cout<<"test"<<std::endl;
    }

    bool PlaceQueueOnRow(int idx){
      for(int i = 0;i<m_board_size; ++i){
        if (QueueExist(idx, i))
          continue;
        PlaceQueueOnPos(idx, i);
      }
      return true;
    }

    void PlaceQueueOnPos(int row, int col){
      int cnt =0;
      {     
        //PerformanceHelper ph("abc");
        PlaceQueueOnPosInternal(row, col, cnt);
      }
      QueueEightDelegate::OnCalcComplete(cnt);
    }

    int PlaceQueueOnPosInternal(int row, int col, int& cnt){
      if(row == m_board_size-1){
        cnt ++;
      }
      else{
        *(m_board+row*m_board_size+col) = true;              
        QueueEight qe(this);                
        qe.markboard(row, col);
        for (int i = 0;i<m_board_size;++i)
        {          
          if (qe.QueueExist(row+1, i))
            continue;
          qe.PlaceQueueOnPosInternal(row+1, i, cnt);
        }
        *(m_board+row*m_board_size+col) = false;              
      }
      return cnt;
    }

    bool inline QueueExist(int row, int col){
      return *(m_board + row*m_board_size + col);
    }

    void print(){
      printf("**************\n");
      for (int i =0;i<m_board_size; i++)
      {
        for(int j=0;j<m_board_size;j++)
          printf("%4d", *(m_board + m_board_size*i+j) ? 1 : 0);
        printf("\n");
      }
    }

private:
    bool markboard( int row, int col){
        for(int i =row;i<m_board_size;++i){
            *(m_board+i*m_board_size+col) = true;
        }
        for (int i=row+1, j=col-1 ; i<m_board_size && j>=0; ++i, --j)
            *(m_board+i*m_board_size+j)=true;
        for(int i = row+1, j=col+1; i<m_board_size && j<m_board_size; ++i, ++j)
            *(m_board+i*m_board_size+j)=true;
        return true;
    }

private:
    bool* m_board;
    int m_board_size;
};



class ThreadMgr{
public:
  ThreadMgr(int boardSize, int threadCount): m_board_size(boardSize), m_thread_count(threadCount){    
  }

  void Start(){
    m_threads = new Thread*[m_thread_count];
    for (int i = 0;i<m_thread_count; ++i)
    {
      m_threads[i] = new Thread();
      m_threads[i]->Start();
    }
    {
     // PerformanceHelper ph("internal-");
      QueueEight** qes = new QueueEight*[m_board_size];
      int cnt = 0;
      for(int i=0;i<m_board_size; ++i){
        qes[i] = new QueueEight(m_board_size);
        m_threads[i%m_thread_count]->PostJob(new CJob2<QueueEight, int, int>(qes[i], &QueueEight::PlaceQueueOnPos, 0, i));
        //qes[i]->PlaceQueueOnPosInternal(0, i, cnt);
      }    

      for (int i = 0;i<m_thread_count; ++i)
      {      
        m_threads[i]->Finish();
      }
    }
    
    std::cout<< QueueEightDelegate::getCnt() <<std::endl;

  }

private:
  int m_thread_count;
  Thread** m_threads;
  int m_board_size;
};

int main(int argc, char** argv){
  int boardsize= 8;
  int threadcount = 1;
  if(argc ==2)
    boardsize = atoi(argv[1]);
  else if(argc == 3){
    boardsize = atoi(argv[1]);
    threadcount = atoi(argv[2]);
  }
  std::cout<< argc << std::endl;
  {
    PerformanceHelper ph;
    QueueEightDelegate::Init();
    ThreadMgr tm(boardsize, threadcount);
    tm.Start();
  }  
  getchar();
}