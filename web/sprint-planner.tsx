import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function SprintPlanner() {
	return (
		<div className='min-h-screen w-full bg-background p-4 lg:p-8'>
			<div className='grid grid-cols-1 gap-6 lg:grid-cols-[1fr,400px]'>
				{/* Main Content */}
				<div className='space-y-8 rounded-lg border p-6'>
					<div className='space-y-2'>
						<h2 className='text-lg font-semibold'>Sprint 1</h2>
						<p className='text-sm text-muted-foreground'>Dec 22 - Jan 09</p>
					</div>

					{/* Feature 1 */}
					<div className='space-y-4'>
						<div className='space-y-1'>
							<h3 className='font-medium'>Feature 1</h3>
							<p className='text-sm text-muted-foreground'>Feature description</p>
						</div>
						<div className='space-y-2'>
							{['Task 1', 'Task 2', 'Task 3'].map((task, i) => (
								<div key={i} className='rounded-lg border bg-card p-3 text-card-foreground'>
									{task}
								</div>
							))}
						</div>
					</div>

					{/* Feature 2 */}
					<div className='space-y-4'>
						<div className='space-y-1'>
							<div className='flex items-center gap-2'>
								<h3 className='font-medium'>Feature 2</h3>
								<Input className='w-32' />
							</div>
							<p className='text-sm text-muted-foreground'>Feature description</p>
						</div>
						<div className='space-y-2'>
							{['Task 1', 'Task 2'].map((task, i) => (
								<div key={i} className='rounded-lg border bg-card p-3 text-card-foreground'>
									{task}
								</div>
							))}
						</div>
					</div>

					{/* Feature 3 */}
					<div className='space-y-4'>
						<div className='space-y-1'>
							<h3 className='font-medium'>Feature 3</h3>
							<p className='text-sm text-muted-foreground'>Feature description</p>
						</div>
					</div>

					<div className='flex justify-end gap-2'>
						<Button variant='outline'>Add</Button>
						<Button>Generate Tasks</Button>
					</div>
				</div>

				{/* Sidebar */}
				<div className='space-y-6'>
					<Card>
						<CardHeader>
							<CardTitle>Task 1</CardTitle>
						</CardHeader>
						<CardContent className='space-y-6'>
							{/* Task Description */}
							<div className='flex items-center justify-between gap-4'>
								<div className='text-sm font-medium'>Task Description</div>
								<Button variant='outline' size='sm'>
									Generate Subtasks
								</Button>
							</div>

							{/* Subtasks */}
							<div className='space-y-4'>
								<div className='flex items-center justify-between'>
									<div className='font-medium'>Sub tasks</div>
									<Button variant='outline' size='sm'>
										Do research
									</Button>
								</div>
								<div className='space-y-2'>
									{[1, 2, 3, 4].map((num) => (
										<div key={num} className='flex items-center space-x-2'>
											<Checkbox id={`subtask-${num}`} />
											<label
												htmlFor={`subtask-${num}`}
												className='text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'
											>
												Sub task {num}
											</label>
										</div>
									))}
								</div>
							</div>

							{/* Research */}
							<div className='space-y-4'>
								<div className='font-medium'>Research</div>
								<div className='space-y-2'>
									{[1, 2, 3, 4, 5].map((num) => (
										<Input key={num} placeholder={`Research item ${num}`} />
									))}
								</div>
							</div>
						</CardContent>
					</Card>
				</div>
			</div>
		</div>
	);
}
