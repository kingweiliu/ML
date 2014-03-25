#pragma once

#include <Windows.h>
#include <process.h>
#include <iostream>
#include <vector>

class CLock{
public:
  CLock();
  ~CLock();
  void Lock();
  void UnLock();
private:
  CRITICAL_SECTION m_sc;
};

class CAutoLock{
public:
  CAutoLock(CLock* lock) : m_lock(lock){
    m_lock->Lock();
  }
  ~CAutoLock(){
    m_lock->UnLock();
  }
private:
  CLock* m_lock;
};

class CJob
{
public:
  virtual void Run() = 0;
};

template <class T>
class CJob0 : public CJob{
public:
  typedef void (T::*pFunc)();

  CJob0(T* pt, pFunc pfunc):m_pT(pt), m_pFunc(pfunc){}

  void Run(){
    (m_pT->*m_pFunc)();
  }

private:
  T* m_pT;
  pFunc m_pFunc;
};

template <class T, class P1, class P2>
class CJob2 : public CJob{
public:
  typedef void (T::*pFunc)(P1, P2);

  CJob2(T* pt, pFunc pfunc, P1 p1, P2 p2):m_pT(pt), m_pFunc(pfunc), m_p1(p1), m_p2(p2){}

  void Run(){
    (m_pT->*m_pFunc)(m_p1, m_p2);
  }

private:
  T* m_pT;
  pFunc m_pFunc;
  P1 m_p1;
  P2 m_p2;
};

class Thread{
public:
  void Start(){
    m_handleEvent = ::CreateEvent(NULL, FALSE, FALSE, NULL);    
    m_handleThread = (HANDLE)_beginthreadex(NULL, NULL, ThreadFunc, this, 0, NULL);
    WaitForSingleObject(m_handleEvent, INFINITE);
  }

  void Run(){
    std::cout<<"thread run"<<std::endl;  
    while (true)
    {
      WaitForSingleObject(m_handleEvent, INFINITE);
      std::vector<CJob*> jobs;
      {
        CAutoLock autolock(&m_lock);
        jobs.swap(m_vecJobs);
      }
      if (jobs.empty())
      {
        break;
      }
      for (auto iter = jobs.begin();iter!= jobs.end(); ++ iter)
      {
        (*iter)->Run();
      }
    }
  }
  
  void PostJob(CJob* job){
    CAutoLock autolock(&m_lock);
    m_vecJobs.push_back(job);
    ::SetEvent(m_handleEvent);
  }


  class CQuitJob:public CJob{
    void Run(){
      ExitThread(0);
    }
  };


  void PostQuitMsg(){
      PostJob(new CQuitJob);
  }

  void Finish(){
    PostQuitMsg();
    WaitForSingleObject(m_handleThread, INFINITE);
  }

private:

  void ThreadCreated(){
    ::SetEvent(m_handleEvent);
  }

  unsigned int static __stdcall ThreadFunc(void* arg){
    Thread* pThread = (Thread*) arg;
    pThread->ThreadCreated();
    pThread->Run();
    return 0;
  }

  std::vector<CJob*> m_vecJobs;
  HANDLE m_handleThread;  
  HANDLE m_handleEvent;
  CLock m_lock;
};

