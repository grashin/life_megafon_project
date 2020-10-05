import cv2
import numpy as np

class Field:
    def __init__(self, length, width, init_lives):#// инициализация поля
        self.dim_length = length
        self.dim_width = width
        self.field = []
        for i in range(length):
            self.field.append([False] * width)
        for i, value in enumerate(init_lives):
        	self.field[value[1]][value[0]] = True

        
    def count_neighbors(self,i,j):#//подсчет количества живых соседей
        potential_neighbors = []
        for l in range(i-1, i+2):
            for w in range(j-1, j+2):
                potential_neighbors.append((l,w))
        count = 0
        for l, w in potential_neighbors:
            #// проверка существования клетки, 
            #//исключение самой клетки из списка потенциальных соседей и 
            #//проверка наличия дизни в клетке
            if (l in range(0, length)) and (w in range(0,width)) and not(l == i and w == j) and self.field[l][w]:
                count += 1
        return count  
    
    def update(self):#//обновление поля
        field_ = self.field
        for i in range(length):
            for j in range(width):
                if self.field[i][j]:
                	if Life_Field.count_neighbors(i,j) not in [2,3]:
                		field_[i][j] = False #// клетка умерла
                elif Life_Field.count_neighbors(i,j) == 3:
                    field_[i][j] = True #// в клетке зародилась жизнь
        self.field = field_
	#изменение части поля
    def change_value(self, i, j): 
    	field_ = self.field
    	field_[i][j] = True
	# получение значения поля
    def get_value(self, i, j):
    	return self.field[i][j]


# рисование поля
def Draw_Field():
	img = np.zeros((500, 500, 3), np.uint8)
	img[:, :] = (0, 0, 0)
	for i in range(length):
		for j in range(width):
			if Life_Field.get_value(i, j):
				img[int(500*i/length):int(500*(i+1)/length), int(500*j/width):int(500*(j+1)/width)] = (255, 255, 255)
			else:
				img[int(500*i/length):int(500*(i+1)/length), int(500*j/width):int(500*(j+1)/width)] = (0, 0, 0)
	for i in range(length+1):
		cv2.line(img,(0, int(i*500/length)),(500, int(i*500/length)),(255,0,0),5)
	for j in range(width+1):
		cv2.line(img,(int(j*500/width), 0),(int(j*500/width), 500),(255,0,0),5)
	cv2.imshow('Game_of_Life', img)
	cv2.waitKey(1000)

# рисование начального поля для выбора клеток жизни
def Draw_pick_color(img, length, width, pick_field):
	for i in range(length):
		for j in range(width):
			if pick_field.get_value(i, j):
				img[int(500*i/length):int(500*(i+1)/length), int(500*j/width):int(500*(j+1)/width)] = (255, 255, 255)
			else:
				img[int(500*i/length):int(500*(i+1)/length), int(500*j/width):int(500*(j+1)/width)] = (0, 0, 0)
	for i in range(length+1):
		cv2.line(img,(0, int(i*500/length)),(500, int(i*500/length)),(255,0,0),5)
	for j in range(width+1):
		cv2.line(img,(int(j*500/width), 0),(int(j*500/width), 500),(255,0,0),5)
	img[500:600, 0:500] = (0, 0, 255)
	cv2.putText(img, 'Press down to start game', (int(100),  int(550)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (255, 255, 255), 4)
	return img

# получение координаты выбранной ячейки
def get_x_y(event,x,y,flags,param):
	global position_x, position_y, lives
	if event == cv2.EVENT_LBUTTONDOWN:
		lives+=1
		position_x, position_y = x, y

# выбор ячеек на заданном поле
def pick_items(length, width):
	img = np.zeros((600, 500, 3), np.uint8)
	img[:, :] = (0, 0, 0)
	pick_field = Field(length, width, init_lives)

	while True:
		img = Draw_pick_color(img, length, width, pick_field)
		cv2.namedWindow('pick_items')
		cv2.setMouseCallback('pick_items', get_x_y)
		cv2.imshow('pick_items', img)
		cv2.waitKey(10)

		# ожидание первой выбранной ячейки чтобы запустить цикл
		if lives == 0:
			cv2.waitKey(100)
			continue

		to_add_i, to_add_j = int(position_y*length/500), int(position_x*width/500) 
		add_elem = [to_add_j, to_add_i]
		# если значения клика на красной кнопке, значит перейти к игре жизни
		if to_add_i >= length:
			cv2.destroyWindow('pick_items') 
			return init_lives
		if add_elem not in init_lives:
			init_lives.append(add_elem)
			pick_field.change_value(to_add_i, to_add_j)

def main():
	global length, width, Life_Field, init_lives, lives
	lives = 0

	length = int(input("Enter length: "))
	width = int(input("Enter width: "))
	n_iter = int(input("Enter number of iterations: "))

	init_lives = []
	init_lives = pick_items(length, width)

	Life_Field = Field(length, width, init_lives)

	for i in range(n_iter): #n_iter - количество итераций
		Draw_Field()
		Life_Field.update()
		if i == n_iter-1:
			cv2.waitKey(10000)
	print('Done')

if __name__ == '__main__':
	main()

