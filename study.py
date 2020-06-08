
# argparse用法
import argparse

def main():
    parser = argparse.ArgumentParser(description="Demo of argparse")#括号中的参数description可以省略
    parser.add_argument('-n','--name', default=' Li ')
    parser.add_argument('-y','--year', default='20')
    args = parser.parse_args()
    print(args)
    # name = args.name
    # year = args.year
    # print('Hello {}  {}'.format(name,year))

if __name__ == '__main__':
    main()

    '''(tensorflow) E:\Study\Git\gitskills>python study.py -n Mazhongjie --year '23'
Namespace(name='Mazhongjie', year="'23'")
Hello Mazhongjie  '23'
    
    '''

